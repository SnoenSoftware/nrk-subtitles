""" Interface for shows and methods for fetching shows data """
import json
from typing import List, Optional, Union

import requests

from skam.scraper.episode.episode import Episode


class ShowInterface:
    """ Interface for the different kinds of show """

    name: str

    def get_episodes(self, series_number) -> List[Episode]:
        """ Fetch all episodes in a season """
        pass

    def get_available_seasons(self) -> List:
        """ Fetch all available seasons in a show """
        pass

    def get_season_title(self, season_number) -> Optional[str]:
        """ Get the name of a given season """
        pass

    def get_episode(self, season_number, episode_number) -> Optional[Episode]:
        """ Get a singular episode by season and episode number """
        pass

    def get_preceding_episode(self, current_episode: Episode) -> Optional[Episode]:
        """ Get the episode immediately preceding the given episode """
        pass

    def get_following_episode(self, current_episode: Episode) -> Optional[Episode]:
        """ Get the episode immediately following the given episode """
        pass

    def get_season_number(self, episode: Episode) -> Optional[Union[int, str]]:
        """ Find the season number for a given episode """
        pass


def get_show(name: str) -> Optional[ShowInterface]:
    """ Fetch show configuration and instantiate appropriate object """
    # pylint: disable=import-outside-toplevel
    response = requests.get(
        "https://psapi.nrk.no/tv/catalog/series/{name}".format(name=name)
    )
    config = json.loads(response.text)
    if config["seriesType"] == "sequential":
        from .sequential import SequentialShow

        return SequentialShow(config)

    if config["seriesType"] == "standard":
        from .standard import StandardShow

        return StandardShow(config)

    if config["seriesType"] == "news":
        from .news import NewsShow

        return NewsShow(config)
    return None


def load_installments(path: str) -> dict:
    """ Fetch more standard installments given a uri path to nrk """
    response = requests.get("https://psapi.nrk.no{path}".format(path=path))
    return json.loads(response.text)
