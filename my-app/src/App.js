import React, { useState, useEffect } from 'react';
import './style.css';
import Tabs from './components/Tabs';
import Sidebar from './components/Sidebar';
import Grid from './components/Grid';
import MotorContent from './components/MotorContent';
import ManualControl from './components/ManualControl';
//import Spline from '@splinetool/react-spline';


function App() {
    const [activeTab, setActiveTab] = useState(1);

    const handleTabChange = (tabNumber) => {
        setActiveTab(tabNumber);
    };

    useEffect(() => {
        // Initialize default tab
        setActiveTab(1);
    }, []);

    return (
        <div>
            <header className="header-container">
                <h1>Team 21 Mechanical Arm</h1>
                <button className="send-feedback-button">Send Feedback</button>
            </header>

            <Tabs activeTab={activeTab} onTabChange={handleTabChange} />
            <div className="viewing-window">
                {activeTab === 1 && <Sidebar />}
                {activeTab === 2 && <Grid />}
                {activeTab === 3 && <MotorContent />}
                {activeTab === 4 && <div><h2>Our Team</h2><p>Welcome to our team page!</p></div>}
                {activeTab === 5 && <ManualControl />}
            </div>
            <footer className="connection">
                <div className="device-connection-box">
                    <button className="connect-device-button">Connect a Device</button>
                </div>
            </footer>
        </div>
    );
}

export default App;
