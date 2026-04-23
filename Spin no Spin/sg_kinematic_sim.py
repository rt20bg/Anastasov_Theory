import numpy as np
import matplotlib.pyplot as plt

def generate_random_dipoles(n_particles):
    """
    Генерира 3D вектори със случайна ориентация за началния "спин" / магнитен момент
    """
    phi = np.random.uniform(0, 2 * np.pi, n_particles)
    costheta = np.random.uniform(-1, 1, n_particles)
    theta = np.arccos(costheta)
    
    mu_x = np.sin(theta) * np.cos(phi)
    mu_y = np.sin(theta) * np.sin(phi)
    mu_z = costheta
    return np.vstack((mu_x, mu_y, mu_z)).T

def run_simulation(n_particles=5000):
    print(f"Стартиране на симулацията с {n_particles} класически частици...")
    # Начални позиции на частиците (лъчът има малко разпръскване - Гаусово разпределение)
    initial_x = np.random.normal(0, 0.05, n_particles)
    initial_y = np.random.normal(0, 0.05, n_particles)
    
    # Всяка частица влиза със съвършено случайна ориентация на магнитния си момент
    mu_0 = generate_random_dipoles(n_particles)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # ---------------------------------------------------------
    # ЕКСПЕРИМЕНТ 1: Стандартен Щерн-Герлах (Диполен магнит / 2 полюса)
    # ---------------------------------------------------------
    # Полето B е само по вертикалата (ос Y на екрана). 
    final_x_dipole = np.copy(initial_x)
    final_y_dipole = np.copy(initial_y)
    
    for i in range(n_particles):
        # ПРАВИЛО 1 (Кинематична адаптация):
        # Магнитното поле е много силно. Вместо да остане случайно,
        # диполът се преориентира "светкавично" до най-близката стабилна енергийна ос.
        # Ако първоначално е "по-скоро нагоре", застава плътно нагоре (+1)
        # Ако е "по-скоро надолу", застава плътно надолу (-1)
        alignment = 1 if mu_0[i, 1] > 0 else -1 
        
        # Силата F = grad(mu * B). Отклонява частицата нагоре или надолу.
        deflection_y = alignment * 1.5 
        final_y_dipole[i] += deflection_y
    
    ax1.scatter(final_x_dipole, final_y_dipole, s=2, color='blue', alpha=0.3)
    ax1.set_title("Класически Щерн-Герлах (2 магнити)\nКинематично преориентиране -> 2 точки")
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # ---------------------------------------------------------
    # ЕКСПЕРИМЕНТ 2: Квадруполен магнит (4 магнита в кръст)
    # ---------------------------------------------------------
    # Тук полето расте радиално от центъра навън (B = 0 в центъра).
    final_x_quad = np.copy(initial_x)
    final_y_quad = np.copy(initial_y)
    
    for i in range(n_particles):
        pos = np.array([initial_x[i], initial_y[i]])
        r_mag = np.linalg.norm(pos)
        
        if r_mag < 0.001: 
            continue # Пропускаме идеален център (Майораново превъртане / липса на поле)
            
        r_dir = pos / r_mag # Посоката на локалното магнитно поле
        
        # Проекция на началния случаен магнитен момент върху локалното радиално поле
        mu_proj = np.dot([mu_0[i, 0], mu_0[i, 1]], r_dir)
        
        # ПРАВИЛО 1 (Адаптация спрямо геометрията на полето):
        if mu_proj > 0:
            # Преориентира се Успоредно на полето (стабилен минимум на енергията).
            # Става "High-field seeker" (търсещ силно поле).
            # Силата го дърпа към по-силното поле (навън от центъра).
            force_dir = r_dir 
            deflection = 1.0 * force_dir
        else:
            # Преориентира се Анти-успоредно.
            # Става "Low-field seeker" (търсещ слабо поле).
            # Силата го бута към най-слабото поле (към центъра, където е 0).
            force_dir = -r_dir
            # При фокусиране към центъра, отклонението е право пропорционално на разстоянието
            deflection = 2.0 * force_dir * r_mag 
            
        final_x_quad[i] += deflection[0]
        final_y_quad[i] += deflection[1]
        
    ax2.scatter(final_x_quad, final_y_quad, s=2, color='red', alpha=0.3)
    ax2.set_title("Квадруполен магнит (4 магнита)\nКинематично преориентиране -> Точка и Пръстен!")
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    file_path = 'sg_rakts_simulation_results.png'
    plt.savefig(file_path, dpi=150)
    print(f"Симулацията приключи! Резултатът е запазен като: {file_path}")
    plt.show()

if __name__ == "__main__":
    run_simulation()
