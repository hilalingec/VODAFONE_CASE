import redis

import warnings
warnings.filterwarnings('ignore') 


r = redis.Redis(host='redis_server', port=6379, decode_responses=True)

def save_to_redis(person_id: int, data: dict):
    r.hmset(f"user:{person_id}", data)
    r.expire(f"user:{person_id}", 60)  # expire saniye cinsinden burası ne kadar redis cache'te tutacağı 1 dk yeterli test için 

def get_from_redis(person_id: int):
    return r.hgetall(f"user:{person_id}")