import base64
import requests
import os
import time
from PIL import Image, ImageDraw, ImageFont

# Set up directory
IMAGES_DIR = "images"
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# 1. Mermaid Diagrams Generation
diagrams = {
    "title-diagram": """
    graph TB
        A[Autonomous Field Scout] --> B[Remediation Planner]
        B --> C[Safety Verifier]
        C --> D{Human-in-the-Loop}
        D -- Approved --> E[Precision Executor]
        D -- Denied --> F[Safe Rollback]
        E -- Fail --> F
        E -- Success --> G[Project Completed]
        style D fill:#f9f,stroke:#333,stroke-width:4px
    """,
    "architecture-diagram": """
    graph LR
        subgraph LangGraph Orchestrator
            node1[Scout Agent]
            node2[Planner Agent]
            node3[Safety Agent]
            node4[Execution Agent]
            checkpoint[(MemorySaver State)]
        end
        subgraph Simulation Layer
            sensors[Field Sensors/Drones]
            inventory[Inventory DB]
            hardware[Spray Hub]
        end
        node1 <--> sensors
        node2 <--> inventory
        node4 <--> hardware
    """,
    "sequence-diagram": """
    sequenceDiagram
        participant G as StateGraph
        participant S as Scout
        participant P as Planner
        participant H as Human
        participant E as Executor
        
        G->>S: Invoke(field_id)
        S-->>G: Health/Anomalies
        G->>P: Prepare(Resource Reserver)
        P-->>G: Reserved: True
        Note over G,H: Interrupt: Human Review
        H-->>G: Approve
        G->>E: Commit(Spraying)
        E-->>G: Success: True
    """,
    "flow-diagram": """
    flowchart TD
        StartNode([Start]) --> Scout[Drone Scanning]
        Scout --> Plan[Treatment Planning]
        Plan --> CheckInv{Inventory available?}
        CheckInv -- No --> Rollback[Release Locks]
        CheckInv -- Yes --> Safety[Safety verification]
        Safety -- Wind too high --> Rollback
        Safety -- Safe --> Wait[Wait for Human Approval]
        Wait --> Execute[Commit: Execute Spraying]
        Execute -- Success --> EndNode([Success])
        Execute -- Hardware Failure --> Rollback
        Rollback --> EndFailedNode([Failed])
    """
}

def generate_mermaid_diagrams():
    print("Generating Mermaid diagrams...")
    for name, code in diagrams.items():
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"{IMAGES_DIR}/{name}.png", 'wb') as f:
                    f.write(response.content)
                print(f"  Successfully generated {name}.png")
            else:
                print(f"  Failed to generate {name}. Status code: {response.status_code}")
        except Exception as e:
            print(f"  Error generating {name}: {e}")

# 2. High-Fidelity Terminal GIF Generation
def generate_title_gif():
    print("Generating High-Fidelity Terminal GIF...")
    WIDTH, HEIGHT = 800, 500
    BACKGROUND = (30, 30, 30)
    TEXT_COLOR = (240, 240, 240)
    CMD_COLOR = (120, 255, 120)
    HEADER_BG = (50, 50, 50)
    DOT_COLORS = [(255, 95, 86), (255, 189, 46), (40, 201, 64)] # Mac control buttons

    try:
        # Attempt to find a fixed-width font
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 16)
        font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 16)
    except:
        font = ImageFont.load_default()
        font_bold = font

    frames = []

    def draw_mac_terminal(draw):
        # Draw background
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=BACKGROUND)
        # Draw header
        draw.rectangle([0, 0, WIDTH, 30], fill=HEADER_BG)
        # Draw control buttons
        for i, color in enumerate(DOT_COLORS):
            x = 15 + i * 20
            draw.ellipse([x-6, 15-6, x+6, 15+6], fill=color)
        draw.text((WIDTH//2 - 60, 8), "zsh — agri-remediate-ai", font=font, fill=(180, 180, 180))

    # Typing sequence
    full_cmd = "$ python main.py"
    lines = [
        "System: Starting Autonomous Remediation Workflow.",
        "[Node: scout] - Scouting Field-001...",
        "  Scout: Found 2 anomalies. Health score: 0.54",
        "[Node: planner] - Reserving Pesticide-A...",
        "  Planner: Inventory reserved: True",
        "[Node: safety] - Checking wind speed...",
        "  Safety: Wind speed 12.4 km/h. Safe to proceed: True",
        "--- HUMAN INTERRUPT ---",
        "User approved. Resuming execution...",
        "[Node: executor] - Spraying sequence initiated...",
        "  Executor: Treatment successfully applied."
    ]

    # Create frames for typing command
    for i in range(len(full_cmd) + 1):
        img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(img)
        draw_mac_terminal(draw)
        cmd_text = full_cmd[:i]
        draw.text((20, 50), cmd_text, font=font, fill=CMD_COLOR)
        if i < len(full_cmd):
             draw.rectangle([20 + draw.textlength(cmd_text, font=font), 50, 20 + draw.textlength(cmd_text, font=font) + 10, 68], fill=CMD_COLOR) # Blinking cursor
        frames.append(img)
    
    # Stay on full command
    last_frame = frames[-1]
    for _ in range(5): frames.append(last_frame)

    # Show execution lines scrolling
    curr_lines = []
    for line in lines:
        curr_lines.append(line)
        # Create multiple frames for each line addition to simulate scrolling speed
        for _ in range(3):
            img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
            draw = ImageDraw.Draw(img)
            draw_mac_terminal(draw)
            draw.text((20, 50), full_cmd, font=font, fill=CMD_COLOR)
            for idx, l in enumerate(curr_lines):
                draw.text((20, 80 + idx * 25), l, font=font, fill=TEXT_COLOR)
            frames.append(img)
            
    # Add ASCII table output
    ascii_table = [
        "+-----------------+-------------------+",
        "| Field Property  | Status/Value      |",
        "+-----------------+-------------------+",
        "| Health Score    | 0.94 (POST)       |",
        "| Treatment       | Pesticide-A       |",
        "| Result          | SUCCESS           |",
        "| Rollback        | NONE              |",
        "+-----------------+-------------------+"
    ]
    
    img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)
    draw_mac_terminal(draw)
    draw.text((20, 50), full_cmd, font=font, fill=CMD_COLOR)
    for idx, l in enumerate(lines):
        draw.text((20, 80 + idx * 25), l, font=font, fill=TEXT_COLOR)
    
    table_start_y = 80 + len(lines) * 25 + 10
    for idx, row in enumerate(ascii_table):
        draw.text((20, table_start_y + idx * 20), row, font=font, fill=CMD_COLOR)
    
    # Hold for 3 seconds
    for _ in range(30): frames.append(img)

    # 3. Transition to "UI" (Data plots)
    import numpy as np
    import matplotlib.pyplot as plt
    import io

    def create_ui_frame(health_scores_after):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(["Pre", "Post"], [0.54, 0.94], marker='o', color='#78ff78', linewidth=3, markersize=10)
        ax.set_title("Autonomous Health Improvement", color='white')
        ax.set_ylabel("Health Index", color='white')
        ax.set_ylim(0, 1)
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf).resize((WIDTH, HEIGHT))

    ui_frame = create_ui_frame([0.54, 0.94]).convert("RGB")
    # Fade or just transition
    for _ in range(30): frames.append(ui_frame)

    # Optimize and Save as GIF (P-mode with Global Palette)
    print("  Optimizing GIF with global palette...")
    sample = Image.new("RGB", (WIDTH, HEIGHT * 3))
    sample.paste(frames[0], (0,0)); sample.paste(frames[len(frames)//2], (0,HEIGHT)); sample.paste(frames[-1], (0,HEIGHT*2))
    palette = sample.quantize(colors=256, method=2)
    
    # Convert all frames to RGB then to P-mode using global palette (No Dither)
    final_frames = [f.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    final_frames[0].save(f"{IMAGES_DIR}/title-animation.gif", save_all=True, append_images=final_frames[1:], optimize=True, loop=0, duration=100)
    print(f"  Successfully saved {IMAGES_DIR}/title-animation.gif")

if __name__ == "__main__":
    generate_mermaid_diagrams()
    generate_title_gif()
    
    # Final check
    expected = ["title-diagram.png", "architecture-diagram.png", "sequence-diagram.png", "flow-diagram.png", "title-animation.gif"]
    for f in expected:
        path = os.path.join(IMAGES_DIR, f)
        if os.path.exists(path):
            print(f"VERIFIED: {f} exists. Size: {os.path.getsize(path)} bytes")
        else:
            print(f"ERROR: {f} MISSING!")
