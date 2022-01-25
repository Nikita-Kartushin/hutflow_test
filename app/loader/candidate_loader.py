import asyncio

from view import View
from utils import FileUtils
from utils import ExcelUtils
from utils import HuntFlowApi


class CandidateLoader:
    def __init__(self):
        self._my_organizations = self._get_organizations()
        self._my_vacancies = self._get_vacancies()
        self._my_statuses = self._get_statuses()

    async def load(self, path: str, n_row: int, count: int = None):
        """

        :param path:
        :param count:
        :param n_row:
        :return:
        """

        excel_utils = ExcelUtils(path=path, config={})
        candidates_generator = excel_utils.read_candidates(n_row=n_row)

        candidates = next(iter(candidates_generator))

        for candidate in candidates.to_dict('records'):
            organization_id, vacancy_id = self._get_params_for_attach_candidate(candidate.get('Должность'))

            resume = FileUtils.get_candidates_resume(candidate.get('ФИО'), candidate.get('Должность'), path)

            if resume:
                resume = await HuntFlowApi.create_file(resume, organization_id)

            serialize_candidate = View.serialize_candidate(candidate, resume)
            created_candidate = await HuntFlowApi.create_candidate(serialize_candidate, organization_id)

            comment = candidate.get('Комментарий')
            status = self._get_status_by_name(organization_id=organization_id, name=candidate.get('Статус'))

            await HuntFlowApi.add_recruits_to_vacancy(
                status=status,
                comment=comment,
                vacancy_id=vacancy_id,
                organization_id=organization_id,
                candidate_id=created_candidate.get('id'),
                files_ids=[resume.get('id')] if resume else None
            )

    @staticmethod
    def _get_organizations():
        organizations = HuntFlowApi.get_organizations()
        return [organization.get('id') for organization in organizations]

    def _get_vacancies_of_candidates(self):
        pass

    def _get_vacancies(self):
        vacancies = {}
        for organization_id in self._my_organizations:
            _vacancies = HuntFlowApi.get_vacancy(organization_id)
            vacancies[organization_id] = [
                {
                    'id': vacancy.get('id'),
                    'position': vacancy.get('position')}
                for vacancy in _vacancies]

        return vacancies

    def _get_params_for_attach_candidate(self, position):
        for organization_id in self._my_organizations:
            for vacancy in self._my_vacancies.get(organization_id):
                if vacancy:
                    if position == vacancy.get('position'):
                        return organization_id, vacancy.get('id')

    def _get_statuses(self):
        statuses = {}
        for organization_id in self._my_organizations:
            _statuses = HuntFlowApi.get_statuses(organization_id)
            statuses[organization_id] = [
                {
                    'id': status.get('id'),
                    'name': status.get('name')}
                for status in _statuses]

        return statuses

    def _get_status_by_name(self, organization_id: int, name: str):
        _statuses = self._my_statuses.get(organization_id)

        for status in _statuses:
            if status.get('name') == name:
                return status.get('id')

