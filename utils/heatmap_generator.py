import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

class HeatmapGenerator:
    def __init__(self):
        self.bias_categories = ['Gender', 'Age', 'Ethnicity', 'Family', 'Education', 'Socioeconomic']
        self.severity_colors = {
            'High': '#dc3545',    # Red
            'Medium': '#ffc107',  # Yellow
            'Low': '#28a745',     # Green
            'None': '#6c757d'     # Gray
        }
    
    def generate_bias_heatmap(self, interview_data: dict) -> go.Figure:
        """Generate a comprehensive bias heatmap across questions and categories"""
        if not interview_data or not interview_data.get('bias_analysis'):
            return self._create_empty_heatmap("No bias data available yet")
        
        questions = [f"Q{i+1}" for i in range(len(interview_data['questions']))]
        categories = self.bias_categories
        
        # Create severity matrix
        severity_matrix = []
        annotation_matrix = []
        
        for i, bias_report in enumerate(interview_data['bias_analysis']):
            question_severities = []
            question_annotations = []
            
            for category in categories:
                severity = self._get_category_severity(bias_report, category)
                question_severities.append(severity)
                question_annotations.append(severity)
            
            severity_matrix.append(question_severities)
            annotation_matrix.append(question_annotations)
        
        # Convert to numerical values for coloring
        severity_values = {'High': 3, 'Medium': 2, 'Low': 1, 'None': 0}
        numerical_matrix = []
        for row in severity_matrix:
            numerical_row = [severity_values[sev] for sev in row]
            numerical_matrix.append(numerical_row)
        
        # Create heatmap - FIXED: removed 'titleside' property
        fig = go.Figure(data=go.Heatmap(
            z=numerical_matrix,
            x=categories,
            y=questions,
            colorscale=[[0, '#6c757d'], [0.33, '#28a745'], [0.66, '#ffc107'], [1, '#dc3545']],
            hoverongaps=False,
            hovertemplate=(
                '<b>Question %{y}</b><br>' +
                'Category: %{x}<br>' +
                'Severity: %{text}<br>' +
                '<extra></extra>'
            ),
            text=severity_matrix,
            showscale=True,
            colorbar=dict(
                title="Severity",
                tickmode="array",
                tickvals=[0, 1, 2, 3],
                ticktext=["None", "Low", "Medium", "High"]
            )
        ))
        
        fig.update_layout(
            title={
                'text': 'Real-time Bias Detection Heatmap',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Bias Categories',
            yaxis_title='Interview Questions',
            height=500,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def generate_timeline_heatmap(self, bias_history: list) -> go.Figure:
        """Generate timeline heatmap showing bias evolution"""
        if not bias_history or len(bias_history) < 2:
            return self._create_empty_heatmap("Complete more questions to see timeline analysis")
        
        # Prepare timeline data
        timestamps = [entry.get('timestamp', datetime.now()) for entry in bias_history]
        high_counts = [entry.get('high_count', 0) for entry in bias_history]
        medium_counts = [entry.get('medium_count', 0) for entry in bias_history]
        low_counts = [entry.get('low_count', 0) for entry in bias_history]
        
        # Create timeline chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=high_counts,
            mode='lines+markers',
            name='High Severity',
            line=dict(color='#dc3545', width=4),
            marker=dict(size=8, symbol='circle')
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=medium_counts,
            mode='lines+markers',
            name='Medium Severity',
            line=dict(color='#ffc107', width=3),
            marker=dict(size=6, symbol='square')
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=low_counts,
            mode='lines+markers',
            name='Low Severity',
            line=dict(color='#28a745', width=2),
            marker=dict(size=4, symbol='diamond')
        ))
        
        fig.update_layout(
            title={
                'text': 'Bias Detection Timeline',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Interview Timeline',
            yaxis_title='Number of Bias Instances',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def generate_category_distribution(self, category_breakdown: dict) -> go.Figure:
        """Generate pie chart showing bias category distribution"""
        if not category_breakdown or sum(category_breakdown.values()) == 0:
            return self._create_empty_heatmap("No bias categories detected")
        
        categories = []
        counts = []
        colors = ['#dc3545', '#ffc107', '#28a745', '#6f42c1', '#e83e8c', '#fd7e14']
        
        for category, count in category_breakdown.items():
            if count > 0:
                categories.append(category)
                counts.append(count)
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=counts,
            hole=0.4,
            marker=dict(colors=colors[:len(categories)]),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': 'Bias Category Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def generate_severity_gauge(self, overall_score: float) -> go.Figure:
        """Generate gauge chart for overall bias score"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Bias Score", 'font': {'size': 20}},
            delta={'reference': 50, 'increasing': {'color': "#28a745"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#1f77b4"},
                'bgcolor': "black",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': '#dc3545'},
                    {'range': [40, 70], 'color': '#ffc107'},
                    {'range': [70, 100], 'color': '#28a745'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=100, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def _get_category_severity(self, bias_report: dict, category: str) -> str:
        """Get severity for a specific bias category"""
        if not bias_report or not bias_report.get('bias_types'):
            return 'None'
        
        category_lower = category.lower()
        bias_types = bias_report.get('bias_types', [])
        
        for bias_type in bias_types:
            if category_lower in bias_type.lower():
                return bias_report.get('severity', 'Low')
        
        return 'None'
    
    def _create_empty_heatmap(self, message: str) -> go.Figure:
        """Create empty heatmap placeholder"""
        fig = go.Figure()
        fig.update_layout(
            title={
                'text': message,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text=message,
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="white")
            )],
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

# Global heatmap generator instance
heatmap_generator = HeatmapGenerator()