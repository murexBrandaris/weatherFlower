document.addEventListener('DOMContentLoaded', () => {
    // Get sidebar elements
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const closeSidebarBtn = document.getElementById('close-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    // Get climate and season containers
    const climateList = document.getElementById('climate-list');
    const seasonList = document.getElementById('season-list');
    const climateDescription = document.getElementById('climate-description');
    
    // Track current selections
    let currentClimate = null;
    let currentSeason = null;
    const selectedHeader = document.getElementById('selected-climate-season');

    // Helper to update the header
    function updateSelectedHeader() {
        let climateName = '';
        let seasonName = '';
        // Get climate name from active item
        const climateItem = document.querySelector('.climate-item.active');
        if (climateItem) climateName = climateItem.textContent;
        // Get season name from active item
        const seasonItem = document.querySelector('.season-item.active');
        if (seasonItem) seasonName = seasonItem.textContent;
        if (climateName && seasonName) {
            selectedHeader.textContent = `Selected: ${climateName} / ${seasonName}`;
        } else if (climateName) {
            selectedHeader.textContent = `Selected: ${climateName}`;
        } else {
            selectedHeader.textContent = '';
        }
    }
    
    // Function to toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('open');
        if (sidebar.classList.contains('open')) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }
    
    // Event listeners for sidebar toggle
    sidebarToggle.addEventListener('click', toggleSidebar);
    closeSidebarBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
    
    // Function to fetch available climates
    async function fetchClimates() {
        try {
            const response = await fetch('/api/climates');
            const data = await response.json();
            
            // Clear existing items
            climateList.innerHTML = '';
            
            // Add climate items
            Object.entries(data.climates).forEach(([key, name]) => {
                const item = document.createElement('li');
                item.className = 'climate-item';
                item.setAttribute('data-climate', key);
                item.textContent = name;
                
                // Add click event to select climate
                item.addEventListener('click', () => selectClimate(key));
                
                climateList.appendChild(item);
            });
            
            // Select default climate if available
            if (data.defaultClimate && Object.keys(data.climates).includes(data.defaultClimate)) {
                selectClimate(data.defaultClimate);
            }
        } catch (error) {
            console.error('Error fetching climates:', error);
        }
    }
    
    // Function to fetch seasons for a climate
    async function fetchSeasons(climateKey) {
        try {
            const response = await fetch(`/api/seasons?climate=${climateKey}`);
            const data = await response.json();
            
            // Clear existing seasons
            seasonList.innerHTML = '';
            
            // Add season items in specified order if available
            if (Array.isArray(data.seasonOrder)) {
                data.seasonOrder.forEach(key => {
                    const name = data.seasons[key];
                    const item = document.createElement('li');
                    item.className = 'season-item';
                    item.setAttribute('data-season', key);
                    item.textContent = name;
                    // Add click event to select season
                    item.addEventListener('click', () => selectSeason(climateKey, key));
                    seasonList.appendChild(item);
                });
            } else {
                Object.entries(data.seasons).forEach(([key, name]) => {
                    const item = document.createElement('li');
                    item.className = 'season-item';
                    item.setAttribute('data-season', key);
                    item.textContent = name;
                    // Add click event to select season
                    item.addEventListener('click', () => selectSeason(climateKey, key));
                    seasonList.appendChild(item);
                });
            }
            
            // Update climate description
            if (data.description) {
                climateDescription.textContent = data.description;
                climateDescription.style.display = 'block';
            } else {
                climateDescription.style.display = 'none';
            }
            
            // Select default season if available
            if (data.selectedSeason && Object.keys(data.seasons).includes(data.selectedSeason)) {
                selectSeason(climateKey, data.selectedSeason);
            } else if (Object.keys(data.seasons).length > 0) {
                selectSeason(climateKey, Object.keys(data.seasons)[0]);
            }
        } catch (error) {
            console.error('Error fetching seasons:', error);
        }
    }
    
    // Function to select a climate
    function selectClimate(climateKey) {
        // Update active class
        document.querySelectorAll('.climate-item').forEach(item => {
            item.classList.remove('active');
        });
        const selectedItem = document.querySelector(`.climate-item[data-climate="${climateKey}"]`);
        if (selectedItem) {
            selectedItem.classList.add('active');
        }
        // Update current climate and fetch its seasons
        currentClimate = climateKey;
        fetchSeasons(climateKey);
        // Update header (season will be set after fetchSeasons)
        setTimeout(updateSelectedHeader, 0);
    }
    
    // Function to select a season
    async function selectSeason(climateKey, seasonKey) {
        // Update active class
        document.querySelectorAll('.season-item').forEach(item => {
            item.classList.remove('active');
        });
        const selectedItem = document.querySelector(`.season-item[data-season="${seasonKey}"]`);
        if (selectedItem) {
            selectedItem.classList.add('active');
        }
        // Update current season
        currentSeason = seasonKey;
        // Update header
        updateSelectedHeader();
        // Update the hex flower with the new weather state set
        try {
            const response = await fetch('/api/set-weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    climate: climateKey,
                    season: seasonKey
                })
            });
            const data = await response.json();
            if (data.success) {
                // Refresh the hex flower display with new states
                fetchCurrentState();
            } else {
                console.error('Error setting weather:', data.error);
            }
        } catch (error) {
            console.error('Error setting weather:', error);
        }
    }
    
    // Initialize
    fetchClimates();
});
