import os
import socket
import sys

os.environ.pop("GRADIO_SERVER_PORT", None)

import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai

ROLE_PROMPTS = {
    "Product Manager": "As a Product Manager, analyze the following startup idea and provide feedback on product-market fit, user needs, and MVP suggestions.",
    "Investor": "As an Investor, evaluate the following startup idea for market opportunity, scalability, and risks.",
    "Growth Hacker": "As a Growth Hacker, suggest creative growth strategies for the following startup idea.",
    "Technical Advisor": "As a Technical Advisor, evaluate the technical feasibility and architecture recommendations for this startup idea.",
    "Marketing Expert": "As a Marketing Expert, suggest marketing strategies and customer acquisition approaches for this startup idea."
}

BUILDER_TEMPLATE = """
Startup Idea Analysis

Problem: {Problem}
Solution: {Solution}
Target Market: {TargetMarket}
Revenue Model: {Revenue}
Competitors: {Competitors}
Execution Plan: {Execution}

Please provide a comprehensive analysis, feedback, and suggestions for improvement.
"""

PITCH_TEMPLATE = """
You are a startup pitch judge. Read the following pitch and provide a score out of 10, with detailed feedback and suggestions for improvement.

Pitch: {pitch}
"""

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY missing in .env file")

genai.configure(api_key=api_key)

def analyze_role(role, idea):
    if not idea:
        return "Please enter a startup idea to get started!"
    try:
        prompt = ROLE_PROMPTS[role] + f"\nStartup Idea:\n{idea}\n"
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def structured_builder(problem, solution, market, revenue, competitors, execution):
    try:
        prompt = BUILDER_TEMPLATE.format(
            Problem=problem or "Not provided",
            Solution=solution or "Not provided",
            TargetMarket=market or "Not provided",
            Revenue=revenue or "Not provided",
            Competitors=competitors or "Not provided",
            Execution=execution or "Not provided"
        )
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

def pitch_simulation(pitch_text):
    if not pitch_text:
        return "Please enter your pitch to get feedback!"
    try:
        prompt = PITCH_TEMPLATE.format(pitch=pitch_text)
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error evaluating pitch: {str(e)}"

def motivation(challenge):
    if not challenge:
        return "Share what's challenging you today, and I'll help motivate you!"
    try:
        prompt = f"""
        I am a startup founder. My challenge is: {challenge}.
        Give me short motivational advice, and an example of a famous startup that failed but later pivoted to success.
        """
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating motivation: {str(e)}"

def is_port_available(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

with gr.Blocks(title="AI Co-Founder Chatbot") as demo:
    gr.Markdown("# 🚀 AI Co-Founder Chatbot")
    gr.Markdown("Get expert feedback on your startup ideas from different perspectives!")
    
    with gr.Tabs():
        with gr.TabItem("🎯 Role Analysis"):
            with gr.Row():
                with gr.Column():
                    role_dropdown = gr.Dropdown(
                        choices=list(ROLE_PROMPTS.keys()),
                        value="Product Manager",
                        label="Choose Expert Role"
                    )
                    idea_input = gr.Textbox(
                        label="Your Startup Idea",
                        placeholder="Describe your startup idea here...",
                        lines=5
                    )
                    analyze_btn = gr.Button("🔍 Analyze", variant="primary")
                
                with gr.Column():
                    role_output = gr.Textbox(
                        label="Expert Feedback",
                        lines=15,
                        interactive=False
                    )
            
            analyze_btn.click(
                fn=analyze_role,
                inputs=[role_dropdown, idea_input],
                outputs=role_output
            )
        
        with gr.TabItem("🏗️ Idea Builder"):
            with gr.Row():
                with gr.Column():
                    problem_input = gr.Textbox(label="Problem", lines=2)
                    solution_input = gr.Textbox(label="Solution", lines=2)
                    market_input = gr.Textbox(label="Target Market", lines=2)
                
                with gr.Column():
                    revenue_input = gr.Textbox(label="Revenue Model", lines=2)
                    competitors_input = gr.Textbox(label="Competitors", lines=2)
                    execution_input = gr.Textbox(label="Execution Plan", lines=2)
            
            build_btn = gr.Button("🔨 Build Analysis", variant="primary")
            builder_output = gr.Textbox(label="Comprehensive Analysis", lines=15, interactive=False)
            
            build_btn.click(
                fn=structured_builder,
                inputs=[problem_input, solution_input, market_input, revenue_input, competitors_input, execution_input],
                outputs=builder_output
            )
        
        with gr.TabItem("🎤 Pitch Judge"):
            pitch_input = gr.Textbox(
                label="Your Pitch",
                placeholder="Enter your startup pitch here...",
                lines=8
            )
            pitch_btn = gr.Button("⚖️ Judge Pitch", variant="primary")
            pitch_output = gr.Textbox(label="Pitch Feedback & Score", lines=10, interactive=False)
            
            pitch_btn.click(
                fn=pitch_simulation,
                inputs=pitch_input,
                outputs=pitch_output
            )
        
        with gr.TabItem("💪 Motivation"):
            challenge_input = gr.Textbox(
                label="What's Your Challenge?",
                placeholder="Share what's challenging you as a founder...",
                lines=4
            )
            motivate_btn = gr.Button("🔥 Get Motivated", variant="primary")
            motivation_output = gr.Textbox(label="Motivational Advice", lines=8, interactive=False)
            
            motivate_btn.click(
                fn=motivation,
                inputs=challenge_input,
                outputs=motivation_output
            )

def launch_app():
    ports_to_try = [7861, 8080, 8000, 5000, 3000, 9000, 8888, 7860]
    
    print("Searching for available port...")
    
    for port in ports_to_try:
        if is_port_available(port):
            try:
                print(f"Launching on port {port}...")
                demo.launch(
                    server_name="127.0.0.1",
                    server_port=port,
                    share=False,
                    inbrowser=True,
                    show_error=True,
                    prevent_thread_lock=False
                )
                print(f"Successfully launched on http://localhost:{port}")
                return
            except Exception as e:
                print(f"Port {port} failed: {str(e)}")
                continue
        else:
            print(f"Port {port} is busy")
    
    print("All ports failed. Try closing other applications or restart your computer.")

if __name__ == "__main__":
    try:
        launch_app()
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)