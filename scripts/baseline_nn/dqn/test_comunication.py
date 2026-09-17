from custom_environment import CustomEnvironment

irradiance_datapaths = ['../../../dataset/csv_41.89109712745386_12.503566993103867_fixed_23_180_PT15M_2024.csv'] * 5
custom_env = CustomEnvironment(
    num_agents=5,
    irradiance_datapaths=irradiance_datapaths,
    delta_time=15*60, proc_interval=60, proc_rate=20, arr_rate=15,
    batteries=[25, 100, 50, 37, 65], panel_surfaces=[1.0, 0.5, 0.75, 0.85, 0.65],
    power_idle=2.6, power_max=6.0, w=1.0
)

# Reset env
obs, _ = custom_env.reset()

print("=== START DEBUG (10 STEP) ===\n")

for step in range(10):
    print(f"--- TIMESTEP {step+1} ---")

    actions = {
        agent: custom_env.action_space(agent).sample()
        for agent in custom_env.possible_agents
    }

    for a_id in custom_env.possible_agents:
        print(
            f" [Node {a_id}] Battery: {custom_env.battery_energies[a_id]:.1f}J |"
            f" Backlog (level): {custom_env.calculate_backlog_level(a_id)}"
        )

    obs, rewards, terminations, truncations, infos = custom_env.step(actions)

    for a_id in custom_env.possible_agents:
        f_i, x_i, g_i, h_i = actions[a_id]

        if x_i == 1: 
            is_success = custom_env.successful_offloads[a_id]
            print(
                f" -> Sender node {a_id} tries to send to node {g_i} | channel successful:"
                f" {is_success}"
            )
        elif x_i == 2:  
            is_success_sender = custom_env.successful_offloads[g_i]
            print(
                f" <- Receiver node {a_id} tries to receive from node {g_i} | Sender channel:"
                f" {is_success_sender}"
            )

    print("-" * 50)