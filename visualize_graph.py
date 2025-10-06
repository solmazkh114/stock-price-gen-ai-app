from src.ai.graph.graph import compiled_graph
from langchain_core.runnables.graph import MermaidDrawMethod

try:
    graph_png = compiled_graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
    
    # Save to file
    with open("graph_visualization.png", "wb") as f:
        f.write(graph_png)
    
    print("Graph saved as 'graph_visualization.png'")
    print("You can open this file with any image viewer to see your LangGraph!")
    
except Exception as e:
    print(f"Error saving graph: {e}")
    print("Make sure you have an internet connection for the Mermaid API")