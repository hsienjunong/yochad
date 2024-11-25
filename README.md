# **Yochad - knockoff Jarvis**

Powered by an **UR3e**, **LLMs**, and questionable brilliance, this system takes your human ramblings, converts them into **sexy robotic commands**, and makes your robot obey you like a you're its master.

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
