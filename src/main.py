
import logging
import sys
import time

from webdriver_manager.chrome import ChromeDriverManager

from notifications import send_push_notification
from scraping import (
    get_offer_links,
    get_offer_states,
    refresh_on_access_denied,
    setup_chrome_webdriver,
    wait_for_page_to_load,
)
from utils import get_pushover_keys, parse_args, setup_logger

urls_to_check = {
    "climbing": "https://ticket-resale.paris2024.org/searchresult/eventseries/3217069?amount=2",
    # "breaking": "https://ticket-resale.paris2024.org/searchresult/eventseries/3217039?amount=2",
    # "concorde": "https://ticket-resale.paris2024.org/searchresult/eventseries/3361036?amount=2"
}

# climbing_urls = [
#     "https://ticket-resale.paris2024.org/tickets/all/1/1/18333297",
#     "https://ticket-resale.paris2024.org/tickets/all/1/1/18333298",
#     "https://ticket-resale.paris2024.org/tickets/all/1/1/18333299",
#     "https://ticket-resale.paris2024.org/tickets/all/1/1/18333300"
# ]


def main(sysargs):
    args = parse_args(sysargs)
    setup_logger(args)
    token, user = get_pushover_keys("pushover_api_keys.json")
    chrome_driver_manager = ChromeDriverManager().install()
    previous_offer_states = {
        key: [] for key in urls_to_check.keys()
    }

    while True:
        try:
            for index, (sport, url) in enumerate(urls_to_check.items()):
                # setup chrome
                driver = setup_chrome_webdriver(chrome_driver_manager)

                # get events page
                logging.info("getting url")
                driver.get(url)
                wait_for_page_to_load(driver)

                # wait patiently in queue
                while driver.current_url != url:
                    logging.info("checking access denied")
                    refresh_on_access_denied(driver)
                    logging.info("sleeping in queue probably ...")
                    time.sleep(1)

                wait_for_page_to_load(driver)

                logging.info(f"current url: {driver.current_url}")
                current_offer_states = get_offer_states(driver)
                logging.info(f"current offer states:\n{current_offer_states}")
                logging.info(f"previous offer states:\n{previous_offer_states[sport]}")

                get_offer_links(driver)
                driver.close()

                number_of_dates_available = len(current_offer_states)

                # notify only on changes to state
                diff_offer_states = [
                    state for state in current_offer_states if state not in previous_offer_states[sport]
                    and state != ""
                ]
                logging.info(f"diff for sport: {sport} \n {diff_offer_states}")

                trigger = len(diff_offer_states) > 0

                # update state
                previous_offer_states[sport] = current_offer_states

                logging.info(f"Number of {sport} dates available: {number_of_dates_available}")
                if trigger:
                    message = {
                        f"New {sport} dates available: {number_of_dates_available}.\nurl: {url}.\nNew states: {diff_offer_states}"
                    }
                    logging.info("Sending push notification ...")
                    send_push_notification(message, token, user)


        except Exception as e:
            logging.info(e)
            message = {f"Something unexpected happened. Error: {e}"}
            driver.close()
            send_push_notification(message, token, user)
            sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
