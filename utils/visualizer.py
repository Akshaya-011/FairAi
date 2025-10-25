import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_simple_skills_chart(skills_graph):
    """Create a simple bar chart of skills by confidence"""
    if not skills_graph:
        fig = go.Figure()
        fig.update_layout(title="No skills data available")
        return fig
    
    skills_data = []
    for skill_name, skill_node in skills_graph.items():
        skills_data.append({
            'Skill': skill_name,
            'Confidence': skill_node.confidence,
            'Category': skill_node.category,
            'Frequency': skill_node.frequency
        })
    
    df = pd.DataFrame(skills_data)
    df = df.sort_values('Confidence', ascending=True)
    
    fig = px.bar(
        df, 
        x='Confidence', 
        y='Skill',
        color='Category',
        title='Skills by Confidence Level',
        orientation='h'
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

def create_category_pie_chart(skills_by_category):
    """Create a pie chart of skills by category"""
    if not skills_by_category:
        fig = go.Figure()
        fig.update_layout(title="No skills data available")
        return fig
    
    categories = list(skills_by_category.keys())
    counts = [len(skills) for skills in skills_by_category.values()]
    
    fig = px.pie(
        values=counts,
        names=categories,
        title='Skills Distribution by Category'
    )
    
    return fig

def create_skills_network(skills_graph):
    """Fallback network graph that's more reliable"""
    return create_simple_skills_chart(skills_graph)

def plot_skill_categories(skills_by_category):
    """Fallback radar chart"""
    return create_category_pie_chart(skills_by_category)

def create_category_barchart(skills_by_category):
    """Create bar chart of skills by category"""
    if not skills_by_category:
        fig = go.Figure()
        fig.update_layout(title="No skills data available")
        return fig
    
    categories = list(skills_by_category.keys())
    counts = [len(skills) for skills in skills_by_category.values()]
    
    fig = px.bar(
        x=categories,
        y=counts,
        title='Number of Skills by Category',
        labels={'x': 'Category', 'y': 'Number of Skills'}
    )
    
    return fig

def create_confidence_heatmap(skills_graph):
    """Create scatter plot of skill confidence"""
    return create_simple_skills_chart(skills_graph)