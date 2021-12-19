from sympy import sqrt, symbols, S, Eq, solve, init_printing, pretty, simplify

init_printing()

print = lambda x, print=print: print(pretty(x))

(
    c,
    h,
    m,
    E_0,
    H,
    N_u2,
    gamma,
    I2,
    I4,
    I5,
    U_0,
    T_0,
    C_u,
    C_q,
    P_gamma,
    Q_x,
    tau_x,
    J_x,
    kappa_x0,
    emit,
) = symbols(
    "c h m E_0 H N_u2 gamma I2 I4 I5 U_0 T_0 C_u C_q P_gamma Q_x tau_x J_x kappa_x0 emit"
)

eq_C_u = Eq(C_u, S(55) / S(24) / sqrt(3))
eq_C_q = Eq(C_q, S(3) * C_u * h / (S(4) * m * c))
eq_P_gamma = Eq(P_gamma, U_0 / T_0)


eq_tau_x = Eq(tau_x, 2 * E_0 / (J_x * P_gamma))
eq_J_x = Eq(J_x, 1 - I4 / I2)


print("from 5.82 to 5.83, is missing a 1 / E^2, subsitute p_gamma from 4.53")

eq_Q_x_1 = Eq(
    Q_x, S(3) / S(2) * C_u * h * c * gamma ** 3 * P_gamma * I5 / I2 / E_0 ** 2
)
eq_Q_x_2 = eq_Q_x_1.subs(P_gamma, 2 * E_0 / J_x / tau_x)
eq_Q_x_3 = eq_Q_x_2.subs(C_u, solve(eq_C_q, C_u)[0])
eq_Q_x_4 = eq_Q_x_3.subs(m, E_0 / gamma / c ** 2)

print(eq_Q_x_1)
print(eq_Q_x_2)
print(eq_Q_x_3)
print(eq_Q_x_4)


print("from 5.82, is missing a 1 / E^2")

eq_Q_x_1 = Eq(
    Q_x, S(3) / S(2) * C_u * h * c * gamma ** 3 * P_gamma * I5 / I2 / E_0 ** 2
)
eq_Q_x_2 = eq_Q_x_1.subs(C_u, solve(eq_C_q, C_u)[0])
eq_Q_x_3 = eq_Q_x_2.subs(P_gamma, eq_P_gamma.rhs)
eq_Q_x_4 = eq_Q_x_3.subs(m, E_0 / gamma / c ** 2)

print(eq_Q_x_1)
print(eq_Q_x_2)
print(eq_Q_x_3)
print(eq_Q_x_4)


print("from 5.83")

eq_Q_x_1 = Eq(Q_x, 4 / tau_x * C_q * gamma ** 2 * I5 / (J_x * I2))
eq_Q_x_2 = eq_Q_x_1.subs(tau_x, eq_tau_x.rhs)
eq_Q_x_3 = eq_Q_x_2.subs(P_gamma, eq_P_gamma.rhs)

print(eq_Q_x_1)
print(eq_Q_x_2)
print(eq_Q_x_3)


print("from 5.41")
L = T_0 * c
eq_N_u2_1 = Eq(
    N_u2, C_u * S(3) / S(2) * h * c * gamma ** 3 * P_gamma * kappa_x0 ** 3 / I2
)
eq_N_u2_2 = eq_N_u2_1.subs(C_u, solve(eq_C_q, C_u)[0])
eq_N_u2_3 = eq_N_u2_2.subs(m, E_0 / gamma / c ** 2)
eq_Q_x_1 = Eq(Q_x, eq_N_u2_3.rhs.subs(kappa_x0 ** 3, I5 / E_0 ** 2))
eq_Q_x_2 = eq_Q_x_1.subs(P_gamma, eq_P_gamma.rhs)

print(eq_N_u2_1)
print(eq_N_u2_2)
print(eq_N_u2_3)
print(eq_Q_x_1)
print(eq_Q_x_2)


print("equilibrium emittance from 5.79")
eq_rad = emit * U_0 * J_x / T_0 / E_0
eq_emit_1 = Eq(Q_x, eq_rad)
eq_emit_2 = Eq(emit, solve(eq_emit_1, emit)[0])
eq_emit_3 = eq_emit_2.subs(Q_x, eq_Q_x_2.rhs)
eq_emit_4 = simplify(eq_emit_3.subs(J_x, eq_J_x.rhs))


print(eq_emit_1)
print(eq_emit_2)
print(eq_emit_3)
print(eq_emit_4)
