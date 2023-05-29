from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import data_processing
from teams.models import Team


class TeamView(APIView):
    def post(self, request):

        team_data = request.data

        try:
            data_processing(team_data)
        except ImpossibleTitlesError as error:
            return Response({"error": error.message}, 400)

        except InvalidYearCupError as error:
            return Response({"error": error.message}, 400)

        except NegativeTitlesError as error:
            return Response({"error": error.message}, 400)

        team = Team.objects.create(
            name=team_data["name"],
            titles=team_data["titles"],
            top_scorer=team_data["top_scorer"],
            fifa_code=team_data["fifa_code"],
            first_cup=team_data["first_cup"]
        )

        return Response(model_to_dict(team), 201)

    def get(self, request):
        teams = Team.objects.all()

        teams_dict = []

        for team in teams:
            teams_dict.append(model_to_dict(team))

        return Response(teams_dict)


class TeamViewId(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)

        return Response(team_dict, 200)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, 200)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.delete()

        return Response(status=204)
