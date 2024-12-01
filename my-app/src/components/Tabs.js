function Tabs({ activeTab, onTabChange }) {
    return (
        <div className="tabs">
            <button 
                className={`tab-button ${activeTab === 1 ? 'active' : ''}`} 
                onClick={() => onTabChange(1)}
            >
                Configuration
            </button>
            <button 
                className={`tab-button ${activeTab === 2 ? 'active' : ''}`} 
                onClick={() => onTabChange(2)}
            >
                Free Movement
            </button>
            <button 
                className={`tab-button ${activeTab === 3 ? 'active' : ''}`} 
                onClick={() => onTabChange(3)}
            >
                Command Center
            </button>
            <button 
                className={`tab-button ${activeTab === 4 ? 'active' : ''}`} 
                onClick={() => onTabChange(4)}
            >
                Our Team
            </button>
            <button 
                className={`tab-button ${activeTab === 5 ? 'active' : ''}`} 
                onClick={() => onTabChange(5)}
            >
                Manual Control
            </button>
        </div>
    );
}

export default Tabs;
