import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from typing import Dict, Any

def create_skills_network(skills_graph: Dict[str, Any]) -> go.Figure:
    """Create an interactive network visualization of skills and their relationships"""
    try:
        # Handle empty graph
        if not skills_graph:
            return create_fallback_chart("No skills data available")
        
        G = nx.Graph()
        
        # Add nodes and edges
        for skill_name, skill_data in skills_graph.items():
            # Handle both object and dictionary formats
            if hasattr(skill_data, 'confidence'):
                confidence = skill_data.confidence
                category = skill_data.category
                related_skills = getattr(skill_data, 'related_skills', [])
            elif isinstance(skill_data, dict):
                confidence = skill_data.get('confidence', 0.5)
                category = skill_data.get('category', 'technical')
                related_skills = skill_data.get('related_skills', [])
            else:
                confidence = 0.5
                category = 'technical'
                related_skills = []
            
            # Add skill node
            G.add_node(skill_name, confidence=confidence, category=category)
            
            # Add edges to related skills
            for related_skill in related_skills:
                if related_skill in skills_graph:
                    G.add_edge(skill_name, related_skill)
        
        # Create positions for nodes
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Extract node positions
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
            # Get node attributes
            node_attrs = G.nodes[node]
            confidence = node_attrs.get('confidence', 0.5)
            category = node_attrs.get('category', 'technical')
            
            # Set color based on category
            color_map = {'technical': '#1f77b4', 'soft': '#ff7f0e', 'other': '#2ca02c'}
            node_color.append(color_map.get(category, '#7f7f7f'))
            
            # Set size based on confidence
            node_size.append(15 + (confidence * 25))
        
        # Create edge traces
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                color=node_color,
                size=node_size,
                line=dict(width=2, color='darkgray')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Skills Relationship Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Node size = Confidence level<br>Color = Skill category",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(size=10)
                           ) ],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           height=500
                       ))
        
        return fig
        
    except Exception as e:
        print(f"Error creating network graph: {e}")
        return create_simple_skills_chart(skills_graph)

def create_simple_skills_chart(skills_graph: Dict[str, Any]) -> go.Figure:
    """Create a simple skills visualization that handles both objects and dictionaries"""
    skills_data = []
    
    for skill_name, skill_node in skills_graph.items():
        # Handle both object and dictionary formats
        if hasattr(skill_node, 'confidence'):
            # It's an object with attributes
            confidence = skill_node.confidence
            category = skill_node.category
            frequency = getattr(skill_node, 'frequency', 1)
        elif isinstance(skill_node, dict):
            # It's a dictionary
            confidence = skill_node.get('confidence', 0.5)
            category = skill_node.get('category', 'technical')
            frequency = skill_node.get('frequency', 1)
        else:
            # Fallback
            confidence = 0.5
            category = 'technical'
            frequency = 1
            
        skills_data.append({
            'Skill': skill_name,
            'Confidence': confidence,
            'Category': category,
            'Frequency': frequency
        })
    
    if not skills_data:
        # Create empty figure if no data
        return create_fallback_chart("No skills data available")
    
    df = pd.DataFrame(skills_data)
    
    # Create bar chart
    fig = px.bar(df, x='Skill', y='Confidence', color='Category',
                 title="Skills Confidence Levels",
                 color_discrete_map={'technical': '#1f77b4', 'soft': '#ff7f0e'})
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=True
    )
    
    return fig

def plot_skill_categories(skills_by_category: Dict[str, list]) -> go.Figure:
    """Create a radar chart showing skill distribution by category"""
    try:
        if not skills_by_category:
            return create_fallback_chart("No category data available")
            
        categories = list(skills_by_category.keys())
        skill_counts = [len(skills) for skills in skills_by_category.values()]
        
        # Add first element at the end to close the radar chart
        categories_closed = categories + [categories[0]]
        counts_closed = skill_counts + [skill_counts[0]]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=counts_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(31, 119, 180, 0.3)',
            line=dict(color='#1f77b4'),
            name='Skills Distribution'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(skill_counts) + 1 if skill_counts else 1]
                ),
                angularaxis=dict(
                    rotation=90,
                    direction="clockwise"
                )
            ),
            showlegend=False,
            title="Skills Distribution by Category",
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error creating radar chart: {e}")
        return create_fallback_chart("Radar chart not available")

def create_category_barchart(skills_by_category: Dict[str, list]) -> go.Figure:
    """Create a bar chart showing skill counts by category"""
    try:
        if not skills_by_category:
            return create_fallback_chart("No category data available")
            
        categories = list(skills_by_category.keys())
        skill_counts = [len(skills) for skills in skills_by_category.values()]
        
        # Create color mapping
        color_map = {'technical': '#1f77b4', 'soft': '#ff7f0e'}
        colors = [color_map.get(cat.lower(), '#2ca02c') for cat in categories]
        
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=skill_counts,
            marker_color=colors,
            text=skill_counts,
            textposition='auto',
        )])
        
        fig.update_layout(
            title="Skills Count by Category",
            xaxis_title="Category",
            yaxis_title="Number of Skills",
            showlegend=False,
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error creating category barchart: {e}")
        return create_fallback_chart("Category chart not available")

def create_confidence_heatmap(skills_graph: Dict[str, Any]) -> go.Figure:
    """Create a heatmap showing skill confidence levels"""
    try:
        if not skills_graph:
            return create_fallback_chart("No skills data available")
            
        # Prepare data for heatmap
        skills_list = []
        categories_list = []
        confidence_list = []
        
        for skill_name, skill_node in skills_graph.items():
            # Handle both object and dictionary formats
            if hasattr(skill_node, 'confidence'):
                confidence = skill_node.confidence
                category = skill_node.category
            elif isinstance(skill_node, dict):
                confidence = skill_node.get('confidence', 0.5)
                category = skill_node.get('category', 'technical')
            else:
                confidence = 0.5
                category = 'technical'
                
            skills_list.append(skill_name)
            categories_list.append(category)
            confidence_list.append(confidence)
        
        # Create a pivot table for heatmap
        df = pd.DataFrame({
            'Skill': skills_list,
            'Category': categories_list,
            'Confidence': confidence_list
        })
        
        # Group by category and calculate average confidence
        category_stats = df.groupby('Category').agg({
            'Confidence': 'mean',
            'Skill': 'count'
        }).reset_index()
        
        category_stats = category_stats.rename(columns={'Skill': 'Count'})
        
        # Create heatmap-like visualization
        fig = go.Figure(data=go.Bar(
            x=category_stats['Category'],
            y=category_stats['Confidence'],
            text=[f"Avg: {conf:.2f}<br>Skills: {count}" 
                  for conf, count in zip(category_stats['Confidence'], category_stats['Count'])],
            textposition='auto',
            marker_color=category_stats['Confidence'],
            marker_colorscale='Viridis',
            hovertemplate='<b>%{x}</b><br>Average Confidence: %{y:.2f}<br>Number of Skills: %{customdata}<extra></extra>',
            customdata=category_stats['Count']
        ))
        
        fig.update_layout(
            title="Average Confidence by Skill Category",
            xaxis_title="Category",
            yaxis_title="Average Confidence",
            yaxis_range=[0, 1],
            height=400
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating confidence heatmap: {e}")
        return create_fallback_chart("Confidence heatmap not available")

def create_fallback_chart(message: str) -> go.Figure:
    """Create a simple fallback chart when data is not available"""
    fig = go.Figure()
    fig.update_layout(
        title=message,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16)
        )],
        height=400
    )
    return fig

# For backward compatibility
def create_skills_network_fallback(skills_graph):
    """Alias for backward compatibility"""
    return create_skills_network(skills_graph)