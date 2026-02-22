 // Load data from team_metrics.json
        fetch('team_metrics.json')
            .then(response => response.json())
            .then(data => {
                // Update rebound percentage
                document.getElementById('rebound-pct').textContent =
                    data.rebound_percentage + '%';

                // Update total attempts
                document.getElementById('total-attempts').textContent =
                    data.total_good_attempts + '/' + data.total_attempts;

                //Update top performer 
                document.getElementById('top-performer').textContent = data.top_performer;

                const reboundPctElement = document.getElementById('rebound-pct');
                if (data.rebound_percentage >= 65) {
                    reboundPctElement.style.color = 'green';
                } else {
                    reboundPctElement.style.color = 'red';
                }

                console.log('✅ Data loaded successfully:', data);
            })
            .catch(error => {
                console.error('❌ Error loading data:', error);
            });