# define our tools we will provide to model

from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_driver import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()


class CarDetails(enum.Enum):
    """to create enums for Car class , it's so that we can annotate what should be passed to these functions by using this python ENum"""

    VIN = "vin"
    Make = "make"
    Model = "model"
    Year = "year"


# when you write these functions , you do all of the typing for them in Python , so that the model knows what values to pass for the various parameters to these functions when it starts using it as a tool


class AssistantFunc(llm.FunctionContext):
    """we will store some context & it is the car the user is talking about"""

    def __init__(self):
        super().__init__()

        # the reason it is private bcoz you don't want to access this or change this.a convention in python to doesn't try to modify this attribute
        self._car_details = {
            CarDetails.VIN: "",  # we are using Enum , bcox model should always know what field it should be using , when it starts accessing values in this class.
            CarDetails.Make: "",
            CarDetails.Model: "",
            CarDetails.Year: "",
        }  # to store the context of the current car we're looking at

    def get_car_str(self) -> str:
        car_str = ""

        for key, value in self._car_details.items():
            car_str += f"{key}: {value}\n"

        return car_str

    # let's make function that will be used as tools by LLM's
    @llm.ai_callable(description="lookup a car by it's vin")
    def lookup_car(
        self,
        vin: Annotated[str, llm.TypeInfo(description="The vin of the car to lookup")],
    ):
        logger.info("looking up car with vin : %s", {vin})
        result = DB.get_car_by_vin(vin)
        if result is None:
            return "No car found with that vin"

        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.Make: result.make,
            CarDetails.Model: result.model,
            CarDetails.Year: result.year,
        }

        # car_str = ""

        # for key, value in self._car_details.items():
        #     car_str += f"{key}: {value}\n"

        return f"The car details are:{self.get_car_str()}"  # returning to the model as a string instead of python dictionary

    @llm.ai_callable(description="get the details of the current car")
    def get_car_details(self):
        logger.info("get car  details")
        return f"The car details are: {self.get_car_str()}"

    @llm.ai_callable(description="create a new car")
    def create_car(
        self,
        vin: Annotated[str, llm.TypeInfo(description="The vin of the car")],
        make: Annotated[str, llm.TypeInfo(description="The make of the car ")],
        model: Annotated[str, llm.TypeInfo(description="The model of the car")],
        year: Annotated[int, llm.TypeInfo(description="The year of the car")],
    ):
        logger.info(
            "create car - vin: %s, make: %s, model: %s, year: %s",
            vin,
            make,
            model,
            year,
        )
        result = DB.create_car(vin, make, model, year)
        if result is None:
            return "Failed to create car"

        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.Make: result.make,
            CarDetails.Model: result.model,
            CarDetails.Year: result.year,
        }

        return "car created!"

    def has_car(self):
        return self._car_details[CarDetails.VIN] != ""
