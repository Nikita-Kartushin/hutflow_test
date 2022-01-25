class View:
    data = None

    @classmethod
    def serialize_candidate(cls, candidate: dict, resume: dict = None):
        phone = None
        email = None
        photo_id = None
        birthdate_day = None
        birthdate_year = None
        birthdate_month = None

        candidate_name = candidate.get('ФИО')
        candidate_name = candidate_name.split()
        last_name = candidate_name[0]
        first_name = candidate_name[1] if len(candidate_name) > 1 else None
        middle_name = candidate_name[2] if len(candidate_name) > 2 else None

        if resume:
            resume_field = resume.get('fields')
            if resume_field:
                phones = resume_field.get('phones')
                if phones:
                    phone = next(iter(phones))

                email = resume_field.get('email')

                birthdate = resume_field.get('birthdate')
                if birthdate:
                    birthdate_day = birthdate.get('day')
                    birthdate_year = birthdate.get('year')
                    birthdate_month = birthdate.get('month')

                name = resume_field.get('name')
                if name:
                    last_name = name.get('last')
                    first_name = name.get('first')
                    middle_name = name.get('middle')

            photo = resume.get('photo')
            if photo:
                photo_id = photo.get('id')

        serialize_candidate = {
            "last_name": last_name,
            "first_name": first_name if first_name else candidate.get('ФИО').split()[1],
            "middle_name": middle_name,
            "phone": phone,
            "email": email,
            "position": candidate.get('Должность'),
            "company": "ХХ",
            "money": candidate.get('Ожидания по ЗП'),
            "birthday_day": birthdate_day,
            "birthday_month": birthdate_month,
            "birthday_year": birthdate_year,
            "photo": photo_id,
            "externals": [
                {
                    "data": {
                        "body": resume.get('text') if resume else None
                    },
                    "auth_type": "NATIVE",
                    "files": [{'id': resume.get('id')}] if resume else None,
                    "account_source": None
                }
            ]
        }

        return serialize_candidate
