import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class BiasHeatmapGenerator:
    def _init_(self):
        self.bias_categories = ['Gender', 'Age', 'Ethnicity', 'Family', 'Education']
        self.severity_colors = {
            'High': '#dc3545',
            'Medium': '#ffc107', 
            'Low': '#28a745',
            'None': '#6c757d'
        }
    
    def generate_real_time_heatmap(self, interview_data):
        """Generate real-time bias heatmap across questions and categories"""
        if not interview_data or not interview_data.get('bias_analysis'):
            return self._create_empty_heatmap()
        
        # Prepare data for heatmap
        questions = [f"Q{i+1}" for i in range(len(interview_data['questions']))]
        categories = self.bias_categories
        
        # Create severity matrix
        severity_matrix = []
        for i, bias_report in enumerate(interview_data['bias_analysis']):
            question_severities = []
            for category in categories:
                severity = self._get_category_severity(bias_report, category)
                question_severities.append(severity)
            severity_matrix.append(question_severities)
        
        # Convert to numerical values for coloring
        severity_values = {
            'High': 3,
            'Medium': 2,
            'Low': 1,
            'None': 0
        }
        
        numerical_matrix = []
        for row in severity_matrix:
            numerical_row = [severity_values[sev] for sev in row]
            numerical_matrix.append(numerical_row)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=numerical_matrix,
            x=categories,
            y=questions,
            colorscale=[[0, '#6c757d'], [0.33, '#28a745'], [0.66, '#ffc107'], [1, '#dc3545']],
            hoverongaps=False,
            hovertemplate='<b>Question %{y}</b><br>Category: %{x}<br>Severity: %{text}<extra></extra>',
            text=severity_matrix
        ))
        
        fig.update_layout(
            title='Real-time Bias Detection Heatmap',
            xaxis_title='Bias Categories',
            yaxis_title='Interview Questions',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    def generate_trend_analysis(self, bias_history):
        """Generate bias trend analysis over time"""
        if not bias_history or len(bias_history) < 2:
            return self._create_empty_chart()
        
        # Prepare trend data
        timestamps = [entry['timestamp'] for entry in bias_history]
        high_biases = [entry['high_count'] for entry in bias_history]
        medium_biases = [entry['medium_count'] for entry in bias_history]
        low_biases = [entry['low_count'] for entry in bias_history]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=high_biases,
            mode='lines+markers',
            name='High Bias',
            line=dict(color='#dc3545', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=medium_biases,
            mode='lines+markers', 
            name='Medium Bias',
            line=dict(color='#ffc107', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=low_biases,
            mode='lines+markers',
            name='Low Bias',
            line=dict(color='#28a745', width=2)
        ))
        
        fig.update_layout(
            title='Bias Detection Trends Over Time',
            xaxis_title='Time',
            yaxis_title='Number of Bias Instances',
            height=300,
            showlegend=True
        )
        
        return fig
    
    def _get_category_severity(self, bias_report, category):
        """Get severity for a specific bias category"""
        if not bias_report or not bias_report.get('bias_types'):
            return 'None'
        
        category_lower = category.lower()
        bias_types = bias_report.get('bias_types', [])
        
        # Map bias types to categories
        category_mapping = {
            'gender': ['gender'],
            'age': ['age'], 
            'ethnicity': ['ethnicity'],
            'family': ['family'],
            'education': ['education']
        }
        
        for bias_type in bias_types:
            if category_lower in bias_type.lower():
                return bias_report.get('severity', 'Low')
        
        return 'None'
    
    def _create_empty_heatmap(self):
        """Create empty heatmap placeholder"""
        fig = go.Figure()
        fig.update_layout(
            title='No bias data available yet',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Complete some interview questions to see bias analysis",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False
            )],
            height=400
        )
        return fig
    
    def _create_empty_chart(self):
        """Create empty chart placeholder"""
        fig = go.Figure()
        fig.update_layout(
            title='No trend data available yet',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Complete more questions to see trend analysis",
                xref="paper", yref="paper", 
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False
            )],
            height=300
        )
        return fig

# Global instance
bias_heatmap = BiasHeatmapGenerator()