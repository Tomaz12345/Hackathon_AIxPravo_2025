import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { FaCheckCircle, FaTimesCircle, FaExclamationTriangle } from 'react-icons/fa';

const ResultPage = () => {
  const { id } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/results/${id}/`);
        setResult(response.data);
      } catch (err) {
        setError('Failed to load result. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded inline-block">
          {error}
        </div>
        <div className="mt-4">
          <Link to="/checker" className="text-blue-600 hover:text-blue-800">
            Try again
          </Link>
        </div>
      </div>
    );
  }

  const getStatusIcon = (status) => {
    if (status === 'approved') {
      return <FaCheckCircle className="text-green-500 text-4xl" />;
    } else if (status === 'rejected') {
      return <FaTimesCircle className="text-red-500 text-4xl" />;
    } else {
      return <FaExclamationTriangle className="text-yellow-500 text-4xl" />;
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-800">Brand Check Results</h1>
        </div>
        
        <div className="p-6">
          <div className="flex flex-col md:flex-row mb-8">
            <div className="md:w-1/3 mb-4 md:mb-0">
              <img 
                src={`http://localhost:8000${result.logo}`} 
                alt={result.brandName} 
                className="w-48 h-48 object-contain border border-gray-300 rounded mx-auto"
              />
            </div>
            <div className="md:w-2/3">
              <h2 className="text-xl font-bold mb-2">{result.brandName}</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-600 font-semibold">Territories:</p>
                  <p className="mb-2">{result.territories}</p>
                </div>
                <div>
                  <p className="text-gray-600 font-semibold">Office:</p>
                  <p className="mb-2">{result.office}</p>
                </div>
                <div className="md:col-span-2">
                  <p className="text-gray-600 font-semibold">Goods and Services:</p>
                  <p className="mb-2">{result.goodsServices}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mb-8">
            <div className="flex items-center mb-4">
              {getStatusIcon(result.status)}
              <h3 className="text-xl font-bold ml-3">
                {result.status === 'approved' 
                  ? 'Your brand appears eligible for registration!' 
                  : result.status === 'rejected'
                  ? 'Your brand may face registration challenges.'
                  : 'Your brand has some potential issues to consider.'}
              </h3>
            </div>
            <div className="bg-gray-50 p-4 rounded border border-gray-200">
              <p className="text-gray-800 whitespace-pre-line">{result.feedback}</p>
            </div>
          </div>
          
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-bold mb-4">Database Check Results</h3>
            
            <div className="space-y-4">
              <div className="p-4 border border-gray-200 rounded">
                <h4 className="font-bold">EUIPO (EU Intellectual Property Office)</h4>
                <p>{result.euipoResults}</p>
              </div>
              
              <div className="p-4 border border-gray-200 rounded">
                <h4 className="font-bold">WIPO (World Intellectual Property Organization)</h4>
                <p>{result.wipoResults}</p>
              </div>
              
              <div className="p-4 border border-gray-200 rounded">
                <h4 className="font-bold">Slovenian Intellectual Property Office</h4>
                <p>{result.sipoResults}</p>
              </div>
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <Link
              to="/checker"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline"
            >
              Check Another Brand
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
