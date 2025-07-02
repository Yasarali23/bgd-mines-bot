 import hmac
import hashlib

def get_random_floats(server_seed, client_seed, nonce, count):
    seed = f"{client_seed}:{nonce}"
    h = hmac.new(bytes(server_seed, 'utf-8'), seed.encode(), hashlib.sha256).hexdigest()

    floats = []
    i = 0
    while len(floats) < count:
        sub_hash = h[i:i+5]
        if len(sub_hash) < 5:
            break
        val = int(sub_hash, 16)
        rand_float = val / 0xfffff
        if rand_float < 1:
            floats.append(rand_float)
        i += 5
    return floats

def get_mine_positions(server_seed, client_seed, nonce, mine_count=5):
    floats = get_random_floats(server_seed, client_seed, nonce, 50)
    positions = []
    for f in floats:
        pos = int(f * 25)
        if pos not in positions:
            positions.append(pos)
        if len(positions) == mine_count:
            break
    return [p + 1 for p in positions]
