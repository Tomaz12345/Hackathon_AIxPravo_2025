import React, { useState } from 'react';

const DemoPage = () => {
  const [page, setPage] = useState('home');
  const [logoPreview, setLogoPreview] = useState(null);
  const [formData, setFormData] = useState({
    brandName: '',
    territories: '',
    office: '',
    goodsServices: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  
  const handleLogoChange = (e) => {
    // Simulate file upload with placeholder
    setLogoPreview('/api/placeholder/200/200');
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API request
    setTimeout(() => {
      setIsLoading(false);
      setPage('result');
    }, 1500);
  };
  
  const renderHomePage = () => (
    <div className="bg-white min-h-screen">
      <nav className="bg-gradient-to-r from-blue-600 to-blue-800 p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <div className="text-white font-bold text-2xl flex items-center">
            BrandChecker
          </div>
          <div className="space-x-4">
            <button className="text-white hover:text-blue-200">Home</button>
            <button 
              className="bg-white text-blue-700 px-4 py-2 rounded-md hover:bg-blue-100"
              onClick={() => setPage('checker')}
            >
              Check Brand
            </button>
          </div>
        </div>
      </nav>
      
      <div className="container mx-auto px-4 py-12">
        <section className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-6">
            Check Your Brand's Registration Potential
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Upload your logo and provide brand details to quickly assess if your brand can be registered across multiple trademark databases.
          </p>
          <button 
            onClick={() => setPage('checker')}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-lg text-xl transition-colors duration-300"
          >
            Start Your Brand Check
          </button>
        </section>

        <section className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="text-blue-500 text-4xl mb-4">🖼️</div>
            <h2 className="text-2xl font-bold mb-4">Logo Analysis</h2>
            <p className="text-gray-600">
              Our AI-powered image recognition technology compares your logo against existing trademarks to check for similarities.
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="text-blue-500 text-4xl mb-4">🌎</div>
            <h2 className="text-2xl font-bold mb-4">Global Database Check</h2>
            <p className="text-gray-600">
              We search major trademark databases including EUIPO, WIPO, and national registries to validate your brand's availability.
            </p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="text-blue-500 text-4xl mb-4">🤖</div>
            <h2 className="text-2xl font-bold mb-4">AI Recommendations</h2>
            <p className="text-gray-600">
              Receive intelligent recommendations and insights about your brand's registration potential.
            </p>
          </div>
        </section>
      </div>
      
      <footer className="bg-gray-800 text-white p-4">
        <div className="container mx-auto text-center">
          <p>&copy; 2025 BrandChecker. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
  
  const renderCheckerPage = () => (
    <div className="bg-gray-50 min-h-screen">
      <nav className="bg-gradient-to-r from-blue-600 to-blue-800 p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <div 
            className="text-white font-bold text-2xl flex items-center cursor-pointer"
            onClick={() => setPage('home')}
          >
            BrandChecker
          </div>
          <div className="space-x-4">
            <button 
              className="text-white hover:text-blue-200"
              onClick={() => setPage('home')}
            >
              Home
            </button>
            <button className="bg-white text-blue-700 px-4 py-2 rounded-md">
              Check Brand
            </button>
          </div>
        </div>
      </nav>
      
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <h1 className="text-3xl font-bold text-center mb-8">Check Your Brand</h1>
        
        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6">
          <div className="mb-6">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="logo">
              Brand Logo
            </label>
            <div className="flex items-center space-x-4">
              <button
                type="button"
                onClick={handleLogoChange}
                className="bg-blue-100 hover:bg-blue-200 text-blue-700 font-semibold py-2 px-4 rounded cursor-pointer"
              >
                Choose Logo
              </button>
              <span className="text-gray-600">
                {logoPreview ? 'logo.png' : 'No file chosen'}
              </span>
            </div>
            
            {logoPreview && (
              <div className="mt-4">
                <img src={logoPreview} alt="Logo preview" className="w-40 h-40 object-contain border border-gray-300 rounded" />
              </div>
            )}
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="brandName">
              Brand Name
            </label>
            <input
              type="text"
              id="brandName"
              name="brandName"
              value={formData.brandName}
              onChange={handleInputChange}
              placeholder="e.g. TechNova"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="territories">
              Territories
            </label>
            <input
              type="text"
              id="territories"
              name="territories"
              value={formData.territories}
              onChange={handleInputChange}
              placeholder="e.g. EU, US, China"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="office">
              Office
            </label>
            <input
              type="text"
              id="office"
              name="office"
              value={formData.office}
              onChange={handleInputChange}
              placeholder="e.g. EUIPO, USPTO"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="goodsServices">
              Goods and Services
            </label>
            <textarea
              id="goodsServices"
              name="goodsServices"
              value={formData.goodsServices}
              onChange={handleInputChange}
              rows="4"
              placeholder="Describe the goods and services your brand will provide"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>

          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg focus:outline-none focus:shadow-outline w-full md:w-auto"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Check Brand Availability'}
            </button>
          </div>
        </form>
      </div>
      
      <footer className="bg-gray-800 text-white p-4 mt-auto">
        <div className="container mx-auto text-center">
          <p>&copy; 2025 BrandChecker. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
  
  const renderResultPage = () => (
    <div className="bg-gray-50 min-h-screen">
      <nav className="bg-gradient-to-r from-blue-600 to-blue-800 p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <div 
            className="text-white font-bold text-2xl flex items-center cursor-pointer"
            onClick={() => setPage('home')}
          >
            BrandChecker
          </div>
          <div className="space-x-4">
            <button 
              className="text-white hover:text-blue-200"
              onClick={() => setPage('home')}
            >
              Home
            </button>
            <button 
              className="bg-white text-blue-700 px-4 py-2 rounded-md hover:bg-blue-100"
              onClick={() => setPage('checker')}
            >
              Check Brand
            </button>
          </div>
        </div>
      </nav>
      
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-800">Brand Check Results</h1>
          </div>
          
          <div className="p-6">
            <div className="flex flex-col md:flex-row mb-8">
              <div className="md:w-1/3 mb-4 md:mb-0">
                <img 
                  src="/api/placeholder/200/200" 
                  alt="TechNova Logo" 
                  className="w-48 h-48 object-contain border border-gray-300 rounded mx-auto"
                />
              </div>
              <div className="md:w-2/3">
                <h2 className="text-xl font-bold mb-2">{formData.brandName || "TechNova"}</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-600 font-semibold">Territories:</p>
                    <p className="mb-2">{formData.territories || "EU, USA"}</p>
                  </div>
                  <div>
                    <p className="text-gray-600 font-semibold">Office:</p>
                    <p className="mb-2">{formData.office || "EUIPO"}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-gray-600 font-semibold">Goods and Services:</p>
                    <p className="mb-2">{formData.goodsServices || "Computer software for business management, mobile applications"}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mb-8">
              <div className="flex items-center mb-4">
                <div className="text-yellow-500 text-4xl">⚠️</div>
                <h3 className="text-xl font-bold ml-3">
                  Your brand has some potential issues to consider.
                </h3>
              </div>
              <div className="bg-gray-50 p-4 rounded border border-gray-200">
                <p className="text-gray-800 whitespace-pre-line">
                  Based on our analysis, the brand "{formData.brandName || "TechNova"}" shows moderate potential for registration, but there are some considerations to be aware of:
                  
                  1. There are 2 potentially similar trademarks in the EUIPO database, though they are in different classes than your specified goods and services.
                  
                  2. The WIPO database shows no direct conflicts, which is favorable for international registration.
                  
                  3. No conflicts were found in the Slovenian IP Office database.
                  
                  4. Your logo appears to be distinctive, with no direct visual similarities to registered trademarks.
                  
                  We recommend proceeding with the registration process but consulting with a trademark attorney first to address the potential similarities found in the EUIPO database.
                </p>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-bold mb-4">Database Check Results</h3>
              
              <div className="space-y-4">
                <div className="p-4 border border-gray-200 rounded">
                  <h4 className="font-bold">EUIPO (EU Intellectual Property Office)</h4>
                  <p>Found 2 potentially similar marks to '{formData.brandName || "TechNova"}' in different classes. Further analysis recommended.</p>
                </div>
                
                <div className="p-4 border border-gray-200 rounded">
                  <h4 className="font-bold">WIPO (World Intellectual Property Organization)</h4>
                  <p>No direct conflicts found for '{formData.brandName || "TechNova"}' in the Madrid System database for the specified goods and services.</p>
                </div>
                
                <div className="p-4 border border-gray-200 rounded">
                  <h4 className="font-bold">Slovenian Intellectual Property Office</h4>
                  <p>No existing registrations for '{formData.brandName || "TechNova"}' found in the Slovenian Intellectual Property Office database.</p>
                </div>
              </div>
            </div>
            
            <div className="mt-8 text-center">
              <button
                onClick={() => setPage('checker')}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline"
              >
                Check Another Brand
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <footer className="bg-gray-800 text-white p-4 mt-auto">
        <div className="container mx-auto text-center">
          <p>&copy; 2025 BrandChecker. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
  
  // Render the appropriate page based on state
  switch(page) {
    case 'home':
      return renderHomePage();
    case 'checker':
      return renderCheckerPage();
    case 'result':
      return renderResultPage();
    default:
      return renderHomePage();
  }
};

export default DemoPage;