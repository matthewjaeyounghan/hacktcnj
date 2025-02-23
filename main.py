import os
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def get_api_key():
    """Get OpenAI API key from environment or user input"""
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("\nOpenAI API key not found in environment variables.")
        api_key = input("Please enter your OpenAI API key: ").strip()
        
        if not api_key:
            print("\nError: API key cannot be empty.")
            return None

        # Ask user if they want to save the key
        save_key = input("Would you like to save this API key for future use? (y/n): ").strip().lower()
        if save_key == 'y':
            try:
                with open('.env', 'w') as f:
                    f.write(f'OPENAI_API_KEY={api_key}\n')
                print("\nAPI key saved to .env file.")
            except Exception as e:
                print(f"\nWarning: Could not save API key. Error: {e}")

    return api_key



def generate_manim_script(topic):
    """Generate a Manim script for the given derivative topic"""
    prompt = f"""Create a detailed Manim Python script to teach {topic}. 
    The script should:
    1. Include necessary imports
    2. Create a clear, step-by-step animation
    3. Use appropriate mathematical notation
    4. Follow Manim best practices
    5. Be ready to run without modifications
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "You are a mathematics educator specializing in calculus and Manim animations."
        }, {
            "role": "user",
            "content": prompt
        }]
    )
    
    return response.choices[0].message['content']

def generate_narration_script(topic):
    """Generate a narration script for the derivative topic"""
    prompt = f"""Create a clear and engaging narration script for teaching {topic}.
    The script should:
    1. Explain concepts in a beginner-friendly way
    2. Follow the visual flow of the Manim animation
    3. Include pauses for complex concepts
    4. Use appropriate mathematical terminology
    5. Be only the script, don't add any comments (INCLUDING THE INTRODUCTION, JUST RETURN THE CODE) just the code itself.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "You are a mathematics educator creating clear and engaging narration scripts."
        }, {
            "role": "user",
            "content": prompt
        }]
    )
    
    return response.choices[0].message['content']

def main():
    print("\n=== Derivative Learning Assistant ===\n")
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        return
    
    # Set OpenAI API key
    openai.api_key = api_key
    
    # Get topic from user with validation
    print("\nExample topics: Power Rule, Chain Rule, Product Rule, Quotient Rule")
    topic = input("What derivative topic would you like to learn about? ").strip()
    
    if not topic:
        print("\nError: Topic cannot be empty. Please provide a valid derivative topic.")
        return
    
    print("\nGenerating Manim script...")
    try:
        manim_script = generate_manim_script(topic)
        print("✓ Manim script generated successfully")
        
        print("\nGenerating narration script...")
        narration = generate_narration_script(topic)
        print("✓ Narration script generated successfully")
        
        # Extract scene class name from the generated script
        scene_class = "Scene"  # Default fallback
        for line in manim_script.split('\n'):
            if line.strip().startswith('class') and 'Scene)' in line:
                scene_class = line.split('class ')[-1].split('(')[0].strip()
                break
        
        # Save Manim script
        script_filename = f"derivative_{topic.lower().replace(' ', '_')}_animation.py"
        with open(script_filename, 'w') as f:
            f.write(manim_script)
        
        # Save narration script
        narration_filename = f"derivative_{topic.lower().replace(' ', '_')}_narration.txt"
        with open(narration_filename, 'w') as f:
            f.write(narration)
        
        print("\n=== Generation Complete! ===")
        print(f"\nFiles have been generated:")
        print(f"1. Manim script: {script_filename}")
        print(f"2. Narration script: {narration_filename}")
        print("\nTo run the animation, use the command:")
        print(f"manim -pql {script_filename} {scene_class}")
        
    except Exception as e:
        if 'api_key' in str(e).lower():
            print("\nError: Invalid API key. Please check your OpenAI API key and try again.")
        elif 'rate limit' in str(e).lower():
            print("\nError: OpenAI API rate limit reached. Please wait a moment and try again.")
        elif 'timeout' in str(e).lower():
            print("\nError: Request timed out. Please check your internet connection and try again.")
        else:
            print(f"\nError: {str(e)}")
            print("If the error persists, please check your API key and try again.")

if __name__ == "__main__":
    main()