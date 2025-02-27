import { Link } from 'react-router-dom';
import { FaCheckCircle, FaImage, FaGlobe, FaRobot } from 'react-icons/fa';

const HomePage = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <section className="text-center mb-16">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-6">
          Check Your Brand's Registration Potential
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          Upload your logo and provide brand details to quickly assess if your brand can be registered across multiple trademark databases.
        </p>
        <Link 
          to="/checker" 
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-lg text-xl transition-colors duration-300"
        >
          Start Your Brand Check
        </Link>
      </section>

      <section className="grid md:grid-cols-3 gap-8 mb-16">
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <FaImage className="text-blue-500 text-4xl mb-4" />
          <h2 className="text-2xl font-bold mb-4">Logo Analysis</h2>
          <p className="text-gray-600">
            Our AI-powered image recognition technology compares your logo against existing trademarks to check for similarities.
          </p>
        </div>
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <FaGlobe className="text-blue-500 text-4xl mb-4" />
          <h2 className="text-2xl font-bold mb-4">Global Database Check</h2>
          <p className="text-gray-600">
            We search major trademark databases including EUIPO, WIPO, and national registries to validate your brand's availability.
          </p>
        </div>
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <FaRobot className="text-blue-500 text-4xl mb-4" />
          <h2 className="text-2xl font-bold mb-4">AI Recommendations</h2>
          <p className="text-gray-600">
            Receive intelligent recommendations and insights about your brand's registration potential.
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;