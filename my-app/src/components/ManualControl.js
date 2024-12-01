//<Spline scene="https://prod.spline.design/xFvL2yJD7MTDLpIj/scene.splinecode" />
import React from 'react';
import Spline from '@splinetool/react-spline';

function ManualControl() {
    return (
        <div>
            <h2>Manual Control</h2>
            <p>Use the following keys to operate the mechanical arm:</p>
            <ul>
                <li><strong>W</strong>: Top joint up/down rotation</li>
                <li><strong>A</strong>: Base joint side-to-side rotation</li>
                <li><strong>S</strong>: Middle joint up/down rotation</li>
                <li><strong>D</strong>: Top joint side-to-side rotation</li>
                <li><strong>X</strong>: Lower joint up/down rotation</li>
            </ul>
            <div style={{ height: '1200px', marginTop: '20px' }}>
                <Spline scene="https://prod.spline.design/xFvL2yJD7MTDLpIj/scene.splinecode" />
            </div>
        </div>
    );
}

export default ManualControl;
