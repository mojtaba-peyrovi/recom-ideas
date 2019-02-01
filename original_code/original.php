<?php

namespace HQ\HotelIndexes;

use Models\Hotel;
use Models\HotelScoringSystemInventory;

class HotelIndexesUpdater
{
    private $hotelEntity;
    private $hotelScoringSystemInventory;

    public function __construct(
        Hotel $hotelEntity,
        HotelScoringSystemInventory $hotelScoringSystemInventory
    )
    {
        $this->hotelEntity = $hotelEntity;
        $this->hotelScoringSystemInventory = $hotelScoringSystemInventory;
    }

    public function updateHotelScoreIndexFromSQL($date = null)
    {
        $checkDate = $date === null ? (new \DateTime)->format('Y-m-d') : $date;
        $updProcessId = __METHOD__;
        $sqlQuery = <<<SQL
			UPDATE hotel
            JOIN (
                SELECT
                 hotel.id as id,
                (IFNULL(MAX(hotel_scoring_system_inventory.source_discount_from_bar_percent), 0) * 100) +
                (IFNULL(hotel_settings.commission_pct, 0) * 100) +
                (IF(hotel_settings.inventory_autoload_enabled_flag=1,500,0)) AS hotel_score_index
                FROM hotel
                LEFT JOIN hotel_scoring_system_inventory on (hotel.id = hotel_scoring_system_inventory.hotel_id)
                LEFT JOIN hotel_settings on (hotel.id = hotel_settings.hotel_id)
                WHERE hotel_scoring_system_inventory.upd_dt > {$this->hotelEntity->quote($checkDate)} - INTERVAL 1 DAY
                  AND hotel_scoring_system_inventory.source_discount_from_bar_percent IS NOT NULL
                GROUP BY hotel.id
            ) xTMP
            SET hotel.hotel_score_index = IFNULL(xTMP.hotel_score_index, 0) ,
                hotel.upd_process_id = {$this->hotelEntity->quote($updProcessId)}
            WHERE xTMP.id = hotel.id
SQL;
        $this->hotelEntity->query($sqlQuery);

        /** BKND-3218: Make sure curated hotels are returned first for best deal filter */
        $sqlQuery2 = <<<SQL
            UPDATE hotel
            SET hotel.hotel_score_index = 0.1 ,
                hotel.upd_process_id = {$this->hotelEntity->quote($updProcessId)}
            WHERE hotel.curated_hotel_flag = 1
              AND hotel.hotel_score_index = 0
SQL;

        $this->hotelEntity->query($sqlQuery2);
    }

    public function updateHotelPriceIndexFromSQL($date = null)
    {
        $checkDate = $date === null ? (new \DateTime)->format('Y-m-d') : $date;
        $updProcessId = __METHOD__;
        $query = <<<SQL
            UPDATE hotel
            JOIN (
                SELECT
                    hotel_id AS id,
                    MAX(source_price_usd) AS hotel_price_index
                FROM `hotel_scoring_system_inventory`
                WHERE hotel_scoring_system_inventory.upd_dt > {$this->hotelEntity->quote($checkDate)} - INTERVAL 1 DAY
                  AND checkout_date = checkin_date + 1
                  AND checkin_date = {$this->hotelEntity->quote($checkDate)}
                  AND source_price_usd IS NOT NULL
                GROUP BY hotel_id
            ) xTMP
            SET hotel.hotel_price_index = xTMP.hotel_price_index,
                hotel.upd_process_id = {$this->hotelEntity->quote($updProcessId)}
            WHERE xTMP.id = hotel.id
SQL;
        $this->hotelEntity->query($query);
    }

    public function deleteOldHotelIndexRecords($date = null)
    {
        $checkDate = $date == null ? 'DATE_SUB(NOW(), INTERVAL 24 HOUR)' : $this->hotelScoringSystemInventory->quote($date);
        $condition = "upd_dt < $checkDate";
        $this->hotelScoringSystemInventory
                ->findAll()
                ->where($condition)
                ->delete();
    }

}
