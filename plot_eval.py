import matplotlib.pyplot as plt #python -m pip install -U matplotlib; if matplotlib not installed run this command in the terminal
import numpy as np

def plot_results(results):
    algorithms = list(results.keys())
    # Prepare data for plotting
    metrics = {
        'Score': [np.mean(results[alg]["scores"]) for alg in algorithms],
        'Time': [np.mean(results[alg]["times"]) for alg in algorithms],
        'Max Nodes': [np.mean(results[alg]["max_nodes"]) for alg in algorithms],
        'Memory (MB)': [np.mean(results[alg]["mem_usage"]) for alg in algorithms]
    }
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Algorithm Performance Comparison', fontsize=16)
    
    # Plot each metric
    for i, (metric_name, values) in enumerate(metrics.items()):
        ax = axes[i//2, i%2]
        bars = ax.bar(algorithms, values, color=plt.cm.Paired(np.arange(len(algorithms))))
        ax.set_title(metric_name)
        ax.set_ylabel(metric_name)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        # Rotate algorithm names if they're long
        plt.sca(ax)
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png')  # Save to file
    plt.show()