'use strict'

const Promise = require('bluebird')
const logger = require('../logger')
const dataStores = require('../datastores')
const {redlock} = dataStores.redisCache

const LOCK_TIME = 5000
const MAX_ATTEMPTS = 3
const ATTEMPT_DELAY = 300

const PROCESS_ID = 'isys-worker:hotel-scoring-system:upsert'
const debug = require('debug')(PROCESS_ID)

module.exports = {
  upsert
}

/**
 * Intentionally don't unlock to prevent to often updates of values of the same unique row
 */
function upsert(lookup, hotelId, sourceDiscountFromBarPercent, sourcePriceUsd, attempt, err) {
  attempt = attempt || 0
  const key = `hotel-scoring-system:upsert:${hotelId}:${lookup.country_code}:${lookup.checkin_date}:${lookup.checkout_date}`

  if (attempt > MAX_ATTEMPTS) {
    logger.error(new Error(`${key} MAX_ATTEMPTS exceeded..`))
    if (err) {
      logger.error(err)
    }

    return Promise.resolve()
  }

  debug(`${key} locking...`)
  //do not lock in case error presented - retry attempt
  const start = err ? Promise.resolve() : redlock.lock(key, LOCK_TIME)

  return start
    .then(() => {
      debug(`${key} locked successfully`)

      return _upsert(lookup, hotelId, sourceDiscountFromBarPercent, sourcePriceUsd)
        .then(() => {
          debug(`${key} upserted successfully`)
        })
        .catch(err => {
          debug(`${key} upsert error: ${err.message}`)

          return Promise.delay(ATTEMPT_DELAY)
            .then(() => upsert(lookup, hotelId, sourceDiscountFromBarPercent, sourcePriceUsd, ++attempt, err))
        })
    }, () => {
      debug(`${key} values are being update by somebody else`)
    })
}


function _upsert(lookup, hotelId, sourceDiscountFromBarPercent, sourcePriceUsd) {
  debug(lookup, hotelId, sourceDiscountFromBarPercent)

  const upsertValue = {
    hotel_id: hotelId,
    checkin_date: lookup.checkin_date,
    checkout_date: lookup.checkout_date,
    market_country_code: lookup.country_code,
    source_discount_from_bar_percent: sourceDiscountFromBarPercent,
    source_price_usd: sourcePriceUsd,
    upd_dt: new Date(),
    upd_process_id: PROCESS_ID
  }

  return dataStores.alice('hotel_scoring_system_inventory')
    .where({
      hotel_id: upsertValue.hotel_id,
      checkin_date: upsertValue.checkin_date,
      checkout_date: upsertValue.checkout_date,
      market_country_code: upsertValue.market_country_code
    })
    .update(upsertValue)
    .then(affectedRow => {
      if (!affectedRow) {
        upsertValue.ins_dt = new Date()
        upsertValue.upd_dt = new Date()
        upsertValue.ins_process_id = PROCESS_ID
        return dataStores.alice('hotel_scoring_system_inventory').insert(upsertValue)
      }
      return affectedRow
    })
}
