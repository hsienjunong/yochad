# **Yochad - knockoff Jarvis**

Powered by an **UR3e**, **LLMs**, and questionable brilliance, this system takes your human ramblings, converts them into **sexy robotic commands**, and makes your robot obey you like you're its master.

---

## **What Can Yochad Do?**
1. **Talk, Think, Command**: Using **LangGraph**, Yochad can:
   - google stuff so your dumbass don’t have to
   - turn “yochad, spin baby spin” into actual robot spinny code

2. **Ultimate Flex**: Yochad translates your nonsense into precision robot movements. Basically, you say it, Yochad does it

---

## **Why Yochad?**
It’s **lazy brilliance in action**. No PhDs or manuals needed—just chat with Yochad and watch it make your **UR3e robot** flex like a champ.

---

## **How to Use Yochad**
1. Clone the repo.
2. Create a `.env` file in the project root with the following keys:
```
   OPENAI_API_KEY=<your_openai_api_key>
   TAVILY_API_KEY=<your_tavily_api_key>
   HOST=<robot_host_ip>
   PORT=<robot_port>
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```
4. Run the main file:
```
py main.py
```
5. Say random stuff and let Yochad work its magic.


## **How to Add Custom Tools**

1. **Write a Function**  
   - Create a Python function for your tool logic.

2. **Add a Docstring**  
   - Include a detailed docstring describing:
     - **What the tool does**.
     - **Arguments** the tool takes and their types.
     - **Return values**, if any.

3. **Wrap with `@tool`**  
   - Add `@tool` above the function definition to register it as a tool.

4. **Example**  
   Here’s an example of a simple tool that multiplies two numbers:
   ```python
   @tool
   def multiply_numbers(a, b):
       """
       Multiplies two numbers.

       Args:
           a (int or float): The first number.
           b (int or float): The second number.

       Returns:
           int or float: The product of the two numbers.
       """
       return a * b
   ```
5. **Add the Tool to the Agent's Tool List**

   - Integrate your new tool into the agent's list of tools.
   - Replace the existing tool list items with your custom tools as needed.

   ```python
   tools = [
       tool1,
       tool2,
       tool3,
       # Add your custom tool
       multiply_numbers,
   ]
   ```

6. **Test the Tool**

   - **Integrate and Test**: Add the tool to Yochad and invoke it using commands to confirm it's functioning correctly.
   