import numpy as np

def lin_decreasing(x, x0, x1):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    y[x <= x0] = 1.0
    m = (x > x0) & (x < x1)
    y[m] = (x1 - x[m])/(x1 - x0)
    y[x >= x1] = 0.0
    return y

def lin_increasing(x, x0, x1):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    y[x <= x0] = 0.0
    m = (x > x0) & (x < x1)
    y[m] = (x[m] - x0)/(x1 - x0)
    y[x >= x1] = 1.0
    return y

# --- Membership functions (sesuai grafik) ---
def mu_perm_turun(x): return lin_decreasing(x, 1000, 3000)
def mu_perm_naik(x):  return lin_increasing(x, 1000, 3000)

def mu_pers_sedikit(x): return lin_decreasing(x, 200, 400)
def mu_pers_sedang(x):
    x = np.asarray(x, dtype=float); y = np.zeros_like(x)
    L = (x > 200) & (x <= 400); y[L] = (x[L]-200)/(400-200)
    R = (x > 400) & (x < 800);  y[R] = (800-x[R])/(800-400)
    y[x == 400] = 1.0
    return y
def mu_pers_banyak(x): return lin_increasing(x, 400, 800)

def mu_prod_berkurang(x): return lin_decreasing(x, 2000, 7000)
def mu_prod_bertambah(x): return lin_increasing(x, 2000, 7000)

def hitung_produksi(permintaan, persediaan):
    # Fuzzify
    p_turun = float(mu_perm_turun(permintaan))
    p_naik  = float(mu_perm_naik(permintaan))
    s_sedikit = float(mu_pers_sedikit(persediaan))
    s_sedang  = float(mu_pers_sedang(persediaan))
    s_banyak  = float(mu_pers_banyak(persediaan))

    # Rules (min for AND)
    r1 = min(p_turun, s_banyak)   # -> BERKURANG
    r2 = min(p_turun, s_sedang)   # -> BERKURANG
    r3 = min(p_turun, s_sedikit)  # -> BERTAMBAH
    r4 = min(p_naik,  s_banyak)   # -> BERKURANG
    r5 = min(p_naik,  s_sedang)   # -> BERTAMBAH
    r6 = min(p_naik,  s_sedikit)  # -> BERTAMBAH

    alpha_berkurang = max(r1, r2, r4)
    alpha_bertambah = max(r3, r5, r6)

    # Aggregate + defuzzify (centroid)
    z = np.linspace(0, 8000, 8001)
    mu_out = np.maximum(
        np.minimum(mu_prod_berkurang(z), alpha_berkurang),
        np.minimum(mu_prod_bertambah(z), alpha_bertambah)
    )
    z_star = np.trapz(mu_out * z, z) / np.trapz(mu_out, z)
    return {
        "derajat": {
            "perm_turun": p_turun, "perm_naik": p_naik,
            "pers_sedikit": s_sedikit, "pers_sedang": s_sedang, "pers_banyak": s_banyak,
            "berkurang": alpha_berkurang, "bertambah": alpha_bertambah
        },
        "produksi": z_star
    }

if __name__ == "__main__":
    hasil = hitung_produksi(permintaan=2000, persediaan=700)
    print(hasil)
