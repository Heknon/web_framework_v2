import unittest

from web_framework_v2.http import HttpMethod
from web_framework_v2.route import Endpoint


class RouteMatching(unittest.TestCase):
    mock_routes = [
        "hockey/database/report",
        "/hockey/database/report",
        "hockey/database/report/",
        "/hockey/database/report/",

        "hockey/player/{name}/score",
        "/hockey/player/{name}/score",
        "hockey/player/{name}/score/",
        "/hockey/player/{name}/score/",

        "hockey/player/{name}",
        "/hockey/player/{name}",
        "hockey/player/{name}/",
        "/hockey/player/{name}/",

        "{game}/player/{name}",
        "/{game}/player/{name}",
        "{game}/player/{name}/",
        "/{game}/player/{name}/",

        "{game}/player/{name}/score",
        "/{game}/player/{name}/score",
        "{game}/player/{name}/score/",
        "/{game}/player/{name}/score/",
    ]

    corresponding_test_routes = [
        "hockey/database/report",
        "/hockey/database/report",
        "hockey/database/report/",
        "/hockey/database/report/",

        "hockey/player/HeKNon/score",
        "/hockey/player/HeKNon/score",
        "hockey/player/HeKNon/score/",
        "/hockey/player/HeKNon/score/",

        "hockey/player/HeKNon",
        "/hockey/player/HeKNon",
        "hockey/player/HeKNon/",
        "/hockey/player/HeKNon/",

        "softBaLl/player/HeKNon",
        "/softBaLl/player/HeKNon",
        "softBaLl/player/HeKNon/",
        "/softBaLl/player/HeKNon/",

        "softBaLl/player/HeKNon/score",
        "/softBaLl/player/HeKNon/score",
        "softBaLl/player/HeKNon/score/",
        "/softBaLl/player/HeKNon/score/",
    ]
    routes = [Endpoint(route, HttpMethod.GET, None) for route in mock_routes]

    def test_route_matching(self):
        for (i, route) in enumerate(self.routes):
            self.assertEqual(
                route.matches_url(self.corresponding_test_routes[i])[0],
                True,
                '"' + self.corresponding_test_routes[i] + '" doesn\'t match route "' + self.mock_routes[i] + '"'
            )

    def test_path_variable_matching(self):
        for (i, route) in enumerate(self.routes):
            if i < 4:
                self.assertEqual(
                    route.matches_url(self.corresponding_test_routes[i])[1],
                    None
                )

                continue
            self.assertEqual(
                route.matches_url(self.corresponding_test_routes[i])[1].get("name"),
                "HeKNon"
            )

            if i > 11:
                self.assertEqual(
                    route.matches_url(self.corresponding_test_routes[i])[1].get("game"),
                    "softBaLl"
                )


if __name__ == '__main__':
    unittest.main()
