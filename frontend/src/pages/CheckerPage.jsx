import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const CheckerPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    brandName: '',
    territories: '',
    goodsServices: '',
  });
  const [logo, setLogo] = useState(null);
  const [logoPreview, setLogoPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleLogoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setLogo(file);
      setLogoPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
  
    // Check if at least one field is filled
    const isFormValid = Object.values(formData).some(value => value.trim() !== '') || logo;
    if (!isFormValid) {
      setError('Please provide at least one of the fields (brand name, territories, goods/services, or logo).');
      setIsLoading(false);
      return;
    }
  
    const submitData = new FormData();
    // Append fields only if they have values
    if (logo) {
      submitData.append('logo', logo);
    }
    Object.keys(formData).forEach(key => {
      if (formData[key].trim() !== '') {
        submitData.append(key, formData[key]);
      }
    });
  
    try {
      const response = await axios.post('http://localhost:8000/api/check-brand/', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      navigate(`/result/${response.data.id}`);
    } catch (err) {
      console.error(err.response ? err.response.data : err);  // Log full error response
      setError('There was an error processing your request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-screen min-h-screen px-8 py-12">
      <h1 className="text-3xl font-bold text-center mb-8">Check Your Brand</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 flex justify-between items-center">
          <span>{error}</span>
          <button
            onClick={() => setError('')}
            className="text-red-700 font-bold px-2 cursor-pointer"
          >
            ✖
          </button>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6 w-full max-w-[500px] min-w-[200px]">
        <div className="mb-6">
          <label className="block text-gray-700 font-bold mb-2" htmlFor="logo">
            Brand Logo
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="file"
              id="logo"
              accept="image/*"
              onChange={handleLogoChange}
              className="hidden"
              />
            <label 
              htmlFor="logo" 
              className="bg-blue-100 hover:bg-blue-200 text-blue-700 font-semibold py-2 px-4 rounded cursor-pointer"
            >
              Choose Logo
            </label>
            <span className="text-gray-600">
              {logo ? logo.name : 'No file chosen'}
            </span>
          </div>
          
          {logoPreview && (
            <div className="mt-4">
              <img src={logoPreview} alt="Logo preview" className="w-48 h-48 object-contain" />
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
            className="bg-blue-100 hover:bg-blue-200 text-blue-700 font-semibold py-2 px-4 rounded"
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : 'Check Brand Availability'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CheckerPage;
