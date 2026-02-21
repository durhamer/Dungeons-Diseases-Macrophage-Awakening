import streamlit as st
import random

# --- 1. 初始化遊戲狀態 (Session State) ---
if 'game_active' not in st.session_state:
    # 玩家狀態
    st.session_state.p_hp = 100
    st.session_state.p_max_hp = 100
    st.session_state.p_mp = 50
    st.session_state.p_max_mp = 50
    st.session_state.p_atk = 15
    st.session_state.p_def = 10
    st.session_state.vit_c_turns = 0  
    
    # 敵人狀態
    st.session_state.e_hp = 40
    st.session_state.e_max_hp = 40
    st.session_state.e_atk = 18
    st.session_state.e_def = 5
    
    st.session_state.log = ["🦠 系統警告：偵測到鼻病毒群入侵！菜鳥巨噬細胞，準備迎戰！"]
    st.session_state.game_active = True

# --- 2. 戰鬥邏輯函式 ---
def add_log(msg):
    st.session_state.log.insert(0, msg)

def enemy_turn():
    if st.session_state.e_hp <= 0:
        return
        
    # 鼻病毒現在有三種行動：攻擊、放毒、或是複製回血！
    action = random.choice(["attack", "oxidative_stress", "rapid_replication"])
    
    if action == "attack":
        raw_dmg = max(1, st.session_state.e_atk - st.session_state.p_def)
        final_dmg = int(raw_dmg * random.uniform(0.9, 1.1))
        st.session_state.p_hp = max(0, st.session_state.p_hp - final_dmg)
        add_log(f"🦠 鼻病毒發動【衝撞】，對你造成了 {final_dmg} 點傷害！")
        
    elif action == "oxidative_stress":
        if st.session_state.vit_c_turns > 0:
            add_log("🛡️ 鼻病毒釋放了【氧化破壞】毒素！但被你的「維他命C抗氧化盾」完美擋下了！零傷害！")
        else:
            final_dmg = 10 
            st.session_state.p_hp = max(0, st.session_state.p_hp - final_dmg)
            add_log(f"⚠️ 鼻病毒釋放【氧化破壞】！無視防禦，造成 {final_dmg} 點真實傷害！細胞膜受損！")
            
    elif action == "rapid_replication":
        heal_amount = 12
        st.session_state.e_hp = min(st.session_state.e_max_hp, st.session_state.e_hp + heal_amount)
        add_log(f"🧬 鼻病毒發動【急速複製】！病毒數量增加，回復了 {heal_amount} 點 HP！快阻止牠！")

    if st.session_state.p_hp <= 0:
        st.session_state.game_active = False
        add_log("💀 巨噬細胞細胞膜破裂... 病毒開始大量複製。遊戲結束！")

def player_attack():
    crit_rate = 0.3 if st.session_state.vit_c_turns > 0 else 0.1
    is_crit = random.random() < crit_rate
    
    raw_dmg = max(1, st.session_state.p_atk - st.session_state.e_def)
    final_dmg = int(raw_dmg * random.uniform(0.9, 1.1))
    
    if is_crit:
        final_dmg = int(final_dmg * 1.5)
        add_log(f"💥 爆擊！巨噬細胞發動【呼吸爆發】！對病毒造成 {final_dmg} 點致命傷害！")
    else:
        add_log(f"⚔️ 巨噬細胞發動【吞噬】，對病毒造成 {final_dmg} 點傷害。")
        
    st.session_state.e_hp = max(0, st.session_state.e_hp - final_dmg)
    
    if st.session_state.vit_c_turns > 0:
        st.session_state.vit_c_turns -= 1
        if st.session_state.vit_c_turns == 0:
            st.session_state.p_def -= 5
            add_log("📉 維他命C的「抗氧化盾」效果結束了。")
            
    if st.session_state.e_hp <= 0:
        st.session_state.game_active = False
        add_log("🎉 勝利！鼻病毒群被完全吞噬！身體恢復健康！")
    else:
        enemy_turn()

def player_skill():
    mp_cost = 25
    if st.session_state.p_mp >= mp_cost:
        st.session_state.p_mp -= mp_cost
        base_dmg = 25 
        final_dmg = int(base_dmg * random.uniform(0.9, 1.1))
        st.session_state.e_hp = max(0, st.session_state.e_hp - final_dmg)
        
        add_log(f"🔥 消耗 {mp_cost} MP！釋放【細胞激素】呼叫支援，對病毒造成 {final_dmg} 點巨大傷害！")
        
        if st.session_state.vit_c_turns > 0:
            st.session_state.vit_c_turns -= 1
            if st.session_state.vit_c_turns == 0:
                st.session_state.p_def -= 5
                
        if st.session_state.e_hp <= 0:
            st.session_state.game_active = False
            add_log("🎉 勝利！鼻病毒群被完全吞噬！身體恢復健康！")
        else:
            enemy_turn()
    else:
        add_log("⚠️ MP 不足！無法釋放【細胞激素】！快吃維他命 B 群補充能量！")

def use_vit_c():
    if st.session_state.vit_c_turns == 0:
        st.session_state.vit_c_turns = 3
        st.session_state.p_def += 5
        add_log("💊 吞下【維他命C】！獲得3回合「抗氧化盾」：防禦力提升，爆擊率大增！")
        enemy_turn()
    else:
        add_log("護盾已經存在，不用重複吃啦！")

def use_vit_b():
    restore_amount = 30
    st.session_state.p_mp = min(st.session_state.p_max_mp, st.session_state.p_mp + restore_amount)
    add_log(f"⚡ 喝下【維他命B群】！能量代謝加速，回復 {restore_amount} 點 MP！")
    enemy_turn()

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- 3. UI 介面佈局 ---
st.set_page_config(page_title="Dungeons & Diseases", layout="centered")
st.title("🛡️ Dungeons & Diseases: Macrophage Awakening")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 巨噬細胞 (你)")
    # 載入巨噬細胞圖片，開啟自適應寬度
    st.image("macrophage.png", use_container_width=True)
    
    st.progress(st.session_state.p_hp / st.session_state.p_max_hp, text=f"HP: {st.session_state.p_hp}/{st.session_state.p_max_hp}")
    st.progress(st.session_state.p_mp / st.session_state.p_max_mp, text=f"MP: {st.session_state.p_mp}/{st.session_state.p_max_mp}")
    
    status = "💪 狀態良好"
    if st.session_state.vit_c_turns > 0:
         status = f"🛡️ 抗氧化盾 (剩餘 {st.session_state.vit_c_turns} 回合)"
    st.caption(f"目前狀態: {status}")

with col2:
    st.subheader("🦠 鼻病毒群 (敵)")
    # 載入鼻病毒圖片，開啟自適應寬度
    st.image("rhinovirus.png", use_container_width=True)
    
    st.progress(st.session_state.e_hp / st.session_state.e_max_hp, text=f"HP: {st.session_state.e_hp}/{st.session_state.e_max_hp}")
    st.caption("特點：數量多、會釋放氧化毒素、會急速複製")

st.markdown("---")

# --- 4. 操作區塊 ---
st.subheader("🎮 選擇行動")
action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(5)

with action_col1:
    st.button("⚔️ 吞噬 (普攻)", on_click=player_attack, disabled=not st.session_state.game_active, use_container_width=True)
with action_col2:
    st.button("🔥 細胞激素 (25MP)", on_click=player_skill, disabled=not st.session_state.game_active, use_container_width=True)
with action_col3:
    st.button("💊 維他命 C", on_click=use_vit_c, disabled=not st.session_state.game_active, use_container_width=True)
with action_col4:
    st.button("⚡ 維他命 B群", on_click=use_vit_b, disabled=not st.session_state.game_active, use_container_width=True)
with action_col5:
    if not st.session_state.game_active:
        st.button("🔄 重新開始", on_click=reset_game, use_container_width=True)

st.markdown("---")

# --- 5. 戰鬥日誌 ---
st.subheader("📜 戰鬥紀錄")
log_container = st.container(height=250)
with log_container:
    for msg in st.session_state.log:
        st.markdown(f"> {msg}")
