// frontend/src/components/PeopleCounter.js
import React, { useState, useEffect } from 'react';
import { Play, Pause, Upload, Settings, ChevronRight, Users, Clock, BarChart3, Calendar, Video } from 'lucide-react';

const PeopleCounter = () => {
  const [currentCount, setCurrentCount] = useState(14);
  const [totalCount, setTotalCount] = useState(127);
  const [timePosition, setTimePosition] = useState(42);
  const [isPaused, setIsPaused] = useState(false);
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [fileInputRef] = useState(React.createRef());
  
  // Mock data for demographics
  const demographics = {
    age: [
      { group: "0-17", count: 23, percent: 18 },
      { group: "18-34", count: 52, percent: 41 },
      { group: "35-54", count: 38, percent: 30 },
      { group: "55+", count: 14, percent: 11 }
    ],
    gender: [
      { type: "Male", count: 69, percent: 54 },
      { type: "Female", count: 58, percent: 46 }
    ]
  };
  
  // Simulated timeline data - people count over time
  const timelineData = Array(100).fill().map((_, i) => {
    return Math.floor(Math.sin(i/10) * 10 + 15);
  });
  
  const handleTimelineChange = (e) => {
    setTimePosition(parseInt(e.target.value));
  };

  const handleUpload = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      // Here we would normally upload the file to the backend
      console.log("File selected:", file.name);
      // For now, we'll just simulate uploading
      alert(`File "${file.name}" selected. In a real implementation, this would be uploaded to the backend.`);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100 font-sans">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-950 p-4 flex justify-between items-center">
        <div className="flex items-center">
          <Users className="text-cyan-400 mr-2" />
          <h1 className="text-xl font-light tracking-wider text-cyan-400">PEOPLE<span className="font-bold">COUNTER</span></h1>
        </div>
        <div className="flex space-x-4">
          <button 
            className={`bg-gray-800 hover:bg-gray-700 text-${isWebcamActive ? 'green' : 'cyan'}-400 p-2 rounded flex items-center mr-2`}
            onClick={() => setIsWebcamActive(!isWebcamActive)}
          >
            <Video size={16} className="mr-2" />
            <span>{isWebcamActive ? 'Disable' : 'Enable'} Webcam</span>
          </button>
          <button className="bg-gray-800 hover:bg-gray-700 text-cyan-400 p-2 rounded flex items-center" onClick={handleUpload}>
            <Upload size={16} className="mr-2" />
            <span>Upload Video</span>
          </button>
          <input 
            type="file" 
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="video/*"
            className="hidden"
          />
          <button className="bg-gray-800 hover:bg-gray-700 p-2 rounded">
            <Settings size={16} />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Video Panel */}
        <div className="flex-1 bg-black relative">
          {/* Video Placeholder */}
          {!isWebcamActive && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-full h-full bg-gradient-to-br from-gray-900 to-black flex items-center justify-center">
                <div className="text-cyan-400 flex flex-col items-center">
                  <Users size={48} />
                  <p className="mt-2 text-sm">Connect webcam or upload video file</p>
                </div>
              </div>
            </div>
          )}
          
          {/* Webcam would be implemented here in a real application */}
          {isWebcamActive && (
            <div className="absolute inset-0 bg-gray-800 flex items-center justify-center">
              <p className="text-cyan-400">Webcam feed would appear here</p>
              {/* In a real implementation, we would use a component like:
              <WebcamCapture onFrame={(data) => {
                setCurrentCount(data.count);
                setTotalCount(prev => prev + data.count);
              }} /> */}
            </div>
          )}
          
          {/* Detection Overlays - These would be dynamic in a real implementation */}
          <div className="absolute top-1/4 left-1/4 w-20 h-40 border-2 border-cyan-400 rounded-lg opacity-60"></div>
          <div className="absolute top-1/3 left-1/2 w-20 h-40 border-2 border-green-400 rounded-lg opacity-60"></div>
          <div className="absolute top-1/2 left-2/3 w-20 h-40 border-2 border-cyan-400 rounded-lg opacity-60"></div>
          
          {/* Live Counter */}
          <div className="absolute top-4 right-4 bg-gray-900 bg-opacity-60 p-3 rounded-lg border border-gray-700 backdrop-blur">
            <div className="text-4xl font-bold text-cyan-400 text-center">{currentCount}</div>
            <div className="text-xs text-center uppercase tracking-wider">Current Count</div>
          </div>
          
          {/* Total Counter */}
          <div className="absolute top-4 left-4 bg-gray-900 bg-opacity-60 p-3 rounded-lg border border-gray-700 backdrop-blur">
            <div className="text-4xl font-bold text-cyan-400 text-center">{totalCount}</div>
            <div className="text-xs text-center uppercase tracking-wider">Total Counted</div>
          </div>
          
          {/* Controls */}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center space-x-4 bg-gray-900 bg-opacity-60 p-2 rounded-full border border-gray-700 backdrop-blur">
            <button 
              onClick={() => setIsPaused(!isPaused)} 
              className="bg-gray-800 hover:bg-gray-700 p-2 rounded-full"
            >
              {isPaused ? <Play size={16} /> : <Pause size={16} />}
            </button>
          </div>
        </div>
        
        {/* Stats Panel */}
        <div className="w-80 bg-gray-900 border-l border-gray-800 overflow-auto">
          <div className="p-4 border-b border-gray-800 bg-gray-950">
            <h2 className="text-lg font-medium flex items-center">
              <BarChart3 size={18} className="mr-2 text-cyan-400" />
              Analytics
            </h2>
          </div>
          
          <div className="p-4 border-b border-gray-800">
            <h3 className="text-sm font-medium text-gray-400 mb-3">CURRENT SCENE</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-3 rounded">
                <div className="text-2xl font-bold text-cyan-400">{currentCount}</div>
                <div className="text-xs text-gray-400">People Present</div>
              </div>
              <div className="bg-gray-800 p-3 rounded">
                <div className="text-2xl font-bold text-green-400">03:42</div>
                <div className="text-xs text-gray-400">Avg. Dwell Time</div>
              </div>
            </div>
          </div>
          
          <div className="p-4 border-b border-gray-800">
            <h3 className="text-sm font-medium text-gray-400 mb-3">DEMOGRAPHICS (CURRENT)</h3>
            
            <div className="mb-4">
              <div className="flex justify-between text-xs mb-1">
                <span>Age Distribution</span>
              </div>
              <div className="w-full h-6 bg-gray-800 rounded-full overflow-hidden flex">
                {demographics.age.map((group, i) => (
                  <div 
                    key={i} 
                    style={{width: `${group.percent}%`}} 
                    className={`h-full ${i === 0 ? 'bg-blue-500' : i === 1 ? 'bg-cyan-500' : i === 2 ? 'bg-teal-500' : 'bg-green-500'}`}
                  ></div>
                ))}
              </div>
              <div className="flex justify-between text-xs mt-1">
                <span>0-17</span>
                <span>18-34</span>
                <span>35-54</span>
                <span>55+</span>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span>Gender Distribution</span>
              </div>
              <div className="w-full h-6 bg-gray-800 rounded-full overflow-hidden flex">
                <div style={{width: `${demographics.gender[0].percent}%`}} className="h-full bg-blue-500"></div>
                <div style={{width: `${demographics.gender[1].percent}%`}} className="h-full bg-pink-500"></div>
              </div>
              <div className="flex justify-between text-xs mt-1">
                <span>Male ({demographics.gender[0].percent}%)</span>
                <span>Female ({demographics.gender[1].percent}%)</span>
              </div>
            </div>
          </div>
          
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-400 mb-3">DEMOGRAPHICS (TOTAL)</h3>
            
            <div className="mb-2">
              <div className="flex justify-between mb-1">
                <span className="text-xs">Age Groups</span>
                <span className="text-xs text-gray-500">Count</span>
              </div>
              {demographics.age.map((group, i) => (
                <div key={i} className="flex justify-between items-center mb-2">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full ${i === 0 ? 'bg-blue-500' : i === 1 ? 'bg-cyan-500' : i === 2 ? 'bg-teal-500' : 'bg-green-500'} mr-2`}></div>
                    <span>{group.group}</span>
                  </div>
                  <span className="text-gray-400">{group.count}</span>
                </div>
              ))}
            </div>
            
            <div>
              <div className="flex justify-between mb-1 mt-4">
                <span className="text-xs">Gender</span>
                <span className="text-xs text-gray-500">Count</span>
              </div>
              {demographics.gender.map((type, i) => (
                <div key={i} className="flex justify-between items-center mb-2">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full ${i === 0 ? 'bg-blue-500' : 'bg-pink-500'} mr-2`}></div>
                    <span>{type.type}</span>
                  </div>
                  <span className="text-gray-400">{type.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      {/* Timeline */}
      <div className="bg-gray-950 border-t border-gray-800 p-4">
        <div className="flex items-center mb-2">
          <Clock size={16} className="mr-2 text-cyan-400" />
          <h3 className="text-sm font-medium">Timeline</h3>
          <span className="ml-auto text-xs text-gray-400">
            <Calendar size={12} className="inline mr-1" />
            {`Showing data for 00:${timePosition.toString().padStart(2, '0')}/03:00`}
          </span>
        </div>
        
        <div className="relative">
          {/* Timeline visualization background */}
          <div className="h-10 w-full bg-gray-800 rounded-md overflow-hidden relative">
            <div className="absolute inset-0 flex items-center">
              {timelineData.map((count, i) => (
                <div 
                  key={i} 
                  style={{
                    height: `${Math.min(count * 3, 100)}%`,
                    width: '1%',
                    backgroundColor: i === timePosition ? '#22D3EE' : `rgba(34, 211, 238, ${count/30})`,
                    transform: i === timePosition ? 'scaleY(1.1)' : ''
                  }}
                  className="mx-px transition-all duration-200"
                ></div>
              ))}
            </div>
          </div>
          
          {/* Timeline scrubber */}
          <input 
            type="range"
            min="0"
            max="99"
            value={timePosition}
            onChange={handleTimelineChange}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          
          {/* Current position indicator */}
          <div 
            className="absolute top-0 w-1 bg-cyan-400 h-10 transition-all duration-100 pointer-events-none"
            style={{
              left: `${timePosition}%`,
              boxShadow: '0 0 10px rgba(34, 211, 238, 0.5)'
            }}
          ></div>
        </div>
        
        {/* Timeline markers */}
        <div className="flex justify-between mt-1 text-xs text-gray-500">
          <span>00:00</span>
          <span>00:45</span>
          <span>01:30</span>
          <span>02:15</span>
          <span>03:00</span>
        </div>
      </div>
    </div>
  );
};

export default PeopleCounter;