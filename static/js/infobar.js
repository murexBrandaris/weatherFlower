document.addEventListener('DOMContentLoaded', () => {
    // Get infobar elements
    const infobar = document.getElementById('infobar');
    const infobarToggle = document.getElementById('infobar-toggle');
    const closeInfobarBtn = document.getElementById('close-infobar');
    const overlay = document.getElementById('infobar-overlay');
    
    // Function to toggle infobar
    function toggleInfobar() {
        infobar.classList.toggle('open');
        if (infobar.classList.contains('open')) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }
    
    // Event listeners for infobar toggle
    infobarToggle.addEventListener('click', toggleInfobar);
    closeInfobarBtn.addEventListener('click', toggleInfobar);
    overlay.addEventListener('click', toggleInfobar);
    
    // Function to update infobar content
    function updateInfoContent() {
        const infoContent = document.getElementById('info-content');
        
        // Basic information section
        const basicInfo = document.createElement('div');
        basicInfo.className = 'infobar-section';
        
        const basicTitle = document.createElement('div');
        basicTitle.className = 'infobar-section-title';
        basicTitle.textContent = 'About Weather Flowers';
        basicInfo.appendChild(basicTitle);
        
        const basicText = document.createElement('p');
    basicText.textContent = 'Weather Flowers use a hexagonal grid to represent weather patterns or other state-driven systems. Each hexagon displays a unique weather state, and transitions between states are determined by specific rules.';
        basicInfo.appendChild(basicText);

        // Probabilities section
        const probInfo = document.createElement('div');
        probInfo.className = 'infobar-section';
        
        const probTitle = document.createElement('div');
        probTitle.className = 'infobar-section-title';
        probTitle.textContent = 'Transitions & Probabilities';
        probInfo.appendChild(probTitle);
        
        const probText = document.createElement('p');
    probText.textContent = 'Transitions are determined by rolling a d6 and a d8. The combined result dictates the direction of movement, with each possible transition having its own probability:';
        probInfo.appendChild(probText);
        
        // Create a table for probabilities
        const probTable = document.createElement('table');
        probTable.style.width = '100%';
        probTable.style.marginTop = '12px';
        probTable.style.marginBottom = '12px';
        probTable.style.borderCollapse = 'collapse';
        
        // Add table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        const headers = ['Direction', 'Dice Total', 'Probability'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            th.style.padding = '8px';
            th.style.textAlign = 'left';
            th.style.borderBottom = '1px solid var(--hex-outline-color)';
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        probTable.appendChild(thead);
        
        // Add table body
        const tbody = document.createElement('tbody');
        
        // Data for the table
        const probabilityData = [
            { direction: 'Upper Right', diceTotal: '2-3', probability: '6%' },
            { direction: 'Lower Right', diceTotal: '4-5', probability: '15%' },
            { direction: 'Down', diceTotal: '6-7', probability: '23%' },
            { direction: 'Stay', diceTotal: '8', probability: '13%'},
            { direction: 'Lower Left', diceTotal: '9-10', probability: '23%' },
            { direction: 'Upper Left', diceTotal: '11-12', probability: '15%' },
            { direction: 'Up', diceTotal: '13-14', probability: '6%' }
        ];
        
        probabilityData.forEach((row, index) => {
            const tr = document.createElement('tr');
            
            // Alternate row background colors for better readability
            if (index % 2 === 1) {
                tr.style.backgroundColor = 'var(--sidebar-item-bg)';
            }
            
            Object.values(row).forEach(cellText => {
                const td = document.createElement('td');
                td.textContent = cellText;
                td.style.padding = '8px';
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        probTable.appendChild(tbody);
        probInfo.appendChild(probTable);
        
        // Add explanation text
    const explainText = document.createElement('p');
    explainText.textContent = 'Each hexagon offers six possible exits, corresponding to its edges. When a random transition occurs, the dice roll selects an exit or keeps the weather unchanged. If a transition would move outside the grid, it wraps around to the opposite side. Some exceptions exist, shown by the looping arrows.';
    probInfo.appendChild(explainText);
        
        // Usage section
        const usageInfo = document.createElement('div');
        usageInfo.className = 'infobar-section';
        
        const usageTitle = document.createElement('div');
        usageTitle.className = 'infobar-section-title';
        usageTitle.textContent = 'How to Use';
        usageInfo.appendChild(usageTitle);
        
        const usageList = document.createElement('ul');
        usageList.style.paddingLeft = '20px';
        
        const usageItems = [
            'Click "Random Transition" to advance to a new weather state according to the transition rules.',
            'Click any hexagon to jump directly to that state.',
            'Use the "Reset" button to return to the starting state.',
            'Open the sidebar to choose different climate types and seasons.'
        ];
        
        usageItems.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            li.style.marginBottom = '8px';
            usageList.appendChild(li);
        });
        
        usageInfo.appendChild(usageList);
        
        // Credits section
        const creditsInfo = document.createElement('div');
        creditsInfo.className = 'infobar-section';
        
        const creditsTitle = document.createElement('div');
        creditsTitle.className = 'infobar-section-title';
        creditsTitle.textContent = 'Credits';
        creditsInfo.appendChild(creditsTitle);
        
        const creditsText = document.createElement('p');
        creditsText.innerHTML = "Weather Flowers concept by Goblin's Henchman.<br>App developed by Leth.";
        creditsInfo.appendChild(creditsText);
        
        // Clear and append all sections
        infoContent.innerHTML = '';
        infoContent.appendChild(basicInfo);
        infoContent.appendChild(probInfo);
        infoContent.appendChild(usageInfo);
        infoContent.appendChild(creditsInfo);
    }
    
    // Initialize infobar content
    updateInfoContent();
});
