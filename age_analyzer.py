# -*- coding: utf-8 -*-

import datetime
import math
from statistics import mean, mode, median, harmonic_mean, pvariance
# import matplotlib.pyplot as plt
import requests
import settings


def is_profile_closed(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "",
        "name_case": "Nom"
    })
    data = r.json()['response'][0]

    return not(data['can_access_closed'] or data['is_closed'])


def get_bdate(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "bdate",
        "name_case": "nom"
    })
    try:
        return r.json()['response'][0]['bdate']
    except:
        return -1


def get_name(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "bdate",
        "name_case": "nom"
    })
    try:
        return r.json()['response'][0]
    except:
        return -1


def get_id_by_domain(target):
    r = requests.get("https://api.vk.com/method/users.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_ids": target,
        "fields": "id",
        "name_case": "nom"
    })
    try:
        return r.json()['response'][0]['id']
    except:
        pass


def get_friends(target, count):
    all_data = []
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target,
        "order": "name",
        "count": count,
        "fields": "nickname"
    })
    r = r.json()
    try:
        data = r['response']['items']
    except:
        return -1
    all_data.extend(data)
    if count > 5000:
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "v": settings.version,
            "access_token": settings.token,
            "user_id": target,
            "order": "name",
            "count": count - 5000,
            "offset": 5000,
            "fields": "nickname",
            "name_case": "nom"
        })
        data = r.json()
        try:
            data = data['response']['items']
        except:
            return -1
        all_data.extend(data)
    return all_data


def get_friends_ages(target):
    friends_bdate = get_friends_bdate(target)
    ages = []
    age = -1
    if friends_bdate == "PC":
        return "PC"
    for person in friends_bdate:
        try:
            age = get_age_by_bdate(person['bdate'])
        except:
            pass
        if age != -1:
            ages.append(age)
    return ages


def get_friends_bdate(target):
    target_id = get_id_by_domain(target)
    r = requests.get("https://api.vk.com/method/friends.get", params={
        "v": settings.version,
        "access_token": settings.token,
        "user_id": target_id,
        "order": "name",
        "fields": "bdate",
        "name_case": "nom",
        "count": "10000"
    })
    try:
        return r.json()['response']['items']
    except KeyError:
        return "PC"


def get_age(target):
    birth_date_str = get_bdate(target)
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
    birth_year = int(birth_date_str[length - 4]) * 1000 + int(birth_date_str[length - 3]) * 100 + int(
        birth_date_str[length - 2]) * 10 + int(birth_date_str[length - 1])
    birth_day = int(birth_date_str[0])
    if birth_date_str[1] != '.':  # В дне рождения два символа.
        birth_day *= 10
        birth_day += int(birth_date_str[1])
        if birth_date_str[4] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[3]) * 10 + int(birth_date_str[4])
        else:
            birth_month = int(birth_date_str[3])
    else:  # В дне рождения один символ
        if birth_date_str[3] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[2]) * 10 + int(birth_date_str[3])
        else:  # В месяце рождения один символ
            birth_month = int(birth_date_str[2])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    age = today_date.toordinal() - birth_date.toordinal()
    age = age - age / 366
    age = math.floor(age / 365)
    return age


def get_age_by_bdate(birth_date_str):
    today_date = datetime.datetime.today()
    if birth_date_str == -1:
        return -1
    length = len(birth_date_str)
    if length < 8:
        return -1
    birth_year = int(birth_date_str[length - 4]) * 1000 + int(birth_date_str[length - 3]) * 100 + int(
        birth_date_str[length - 2]) * 10 + int(birth_date_str[length - 1])
    birth_day = int(birth_date_str[0])
    if birth_date_str[1] != '.':  # В дне рождения два символа.
        birth_day *= 10
        birth_day += int(birth_date_str[1])
        if birth_date_str[4] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[3]) * 10 + int(birth_date_str[4])
        else:
            birth_month = int(birth_date_str[3])
    else:  # В дне рождения один символ
        if birth_date_str[3] != '.':  # В месяце рождения два символа
            birth_month = int(birth_date_str[2]) * 10 + int(birth_date_str[3])
        else:  # В месяце рождения один символ
            birth_month = int(birth_date_str[2])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    age = today_date.toordinal() - birth_date.toordinal()
    age = age - age / 366
    age = math.floor(age / 365)
    return age

(ages)
