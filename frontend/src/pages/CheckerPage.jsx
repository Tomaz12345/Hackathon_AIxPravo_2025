import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const CheckerPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    brandName: '',
    territories: '',
    office: '',
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

    const submitData = new FormData();
    submitData.append('logo', logo);
    Object.keys(formData).forEach(key => {
      submitData.append(key, formData[key]);
    });

    try {
      const response = await axios.post('http://localhost:8000/api/check-brand/', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      navigate(`/result/${response.data.id}`);
    } catch (err) {
      setError('There was an error processing your request. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="text-3xl font-bold text-center mb-8">Check Your Brand</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6">
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
              required
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
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
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
            required
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
            required
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
            required
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
  );
};

export default CheckerPage;
