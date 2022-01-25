from io import BytesIO

import requests
from config import config
from aiohttp import FormData
from aiohttp import ClientSession


class HuntFlowApi:
    @classmethod
    async def create_candidate(cls, candidate: dict, organization_id: int):
        url = config.get('url') + f'/account/{organization_id}/applicants'
        headers = {'Authorization': config['token']}

        async with ClientSession() as session:
            response = await session.post(url, json=candidate, headers=headers)
            response = await response.json()

        # response = requests.post(url=url, data=candidate, headers=headers)
        # response = response.json()

        return response

    @classmethod
    async def create_file(cls, file, organization_id: int):
        url = config['url'] + f'/account/{organization_id}/upload'

        headers = {
            'Authorization': config['token'],
            # 'Content-Type': 'multipart/form-data',
            'X-File-Parse': 'true',
        }

        _file = BytesIO(file.read())
        data = FormData()
        data.add_field('file', _file.getvalue())

        async with ClientSession() as session:
            response = await session.post(url, data=data, headers=headers)
            response = await response.json()

        return response

    @classmethod
    def get_organizations(cls):
        url = config.get('url') + '/accounts'
        headers = {'Authorization': config['token']}

        response = requests.get(url, headers=headers)
        response = response.json()

        return response.get('items')

    @classmethod
    async def add_recruits_to_vacancy(
            cls,
            status: str,
            comment: str,
            files_ids: list,
            vacancy_id: int,
            candidate_id: int,
            organization_id: int):
        url = config.get('url') + f'/account/{organization_id}/applicants/{candidate_id}/vacancy'

        headers = {'Authorization': config['token']}

        data = {
            "vacancy": vacancy_id,
            "status": status,
            "comment": comment,
            "files": [{'id': next(iter(files_ids))}],
            "rejection_reason": None,
            "fill_quota": 0
        }

        async with ClientSession() as session:
            response = await session.post(url, json=data, headers=headers)
            response = await response.json()

        return response.get('items')

    @classmethod
    def get_vacancy(cls, organization_id: int):
        url = config.get('url') + f'/account/{organization_id}/vacancies'

        headers = {'Authorization': config['token']}
        params = {'opened': True}

        response = requests.get(url, headers=headers, params=params)
        response = response.json()

        return response.get('items')

    @classmethod
    def get_statuses(cls, organization_id):
        url = config.get('url') + f'/account/{organization_id}/vacancy/statuses'

        headers = {'Authorization': config['token']}

        response = requests.get(url, headers=headers)
        response = response.json()

        return response.get('items')
