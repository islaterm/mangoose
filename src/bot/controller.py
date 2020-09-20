"""
"Mangoose" (c) by Ignacio Slater M.

"Mangoose" is licensed under a
Creative Commons Attribution 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import yaml
from telegram.ext import Dispatcher, Updater

from logs.logger import MangooseLogger


class MangooseBot:
    """
    Main interface of Mangoose
    """
    __dispatcher: Dispatcher
    __logger: MangooseLogger
    __updater: Updater

    def __init__(self, debug: bool = False):
        """
        Setup the parameters and runs a new bot with the token retrieved from the
        config.json file

        :param debug:
            flag that indicates if the bot is running on debug mode
        """
        self.__logger = MangooseLogger(__name__)
        self.__start_updater(debug)
        self.__dispatcher = self.__updater.dispatcher

    def run(self) -> None:
        """ Runs the bot.   """
        self.__logger.info("Starting bot polling service.")
        self.__updater.start_polling()

    def __start_updater(self, debug: bool) -> None:
        """ Starts the bot's updater    """
        self.__logger.info(f"Debug: {debug}")
        with open("tokens.yml", "r") as token_fp:
            tokens = yaml.load(token_fp, yaml.FullLoader)["token"]
            token = tokens["test" if debug else "mangoose"]
        self.__logger.info(f"Starting bot updater")
        self.__updater = Updater(token, use_context=True)
