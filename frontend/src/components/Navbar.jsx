import { Link } from 'react-router-dom';
import { FaCheck } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white font-bold text-2xl flex items-center">
          <FaCheck className="mr-2" />
          BrandChecker
        </Link>
        <div className="space-x-4">
          <Link to="/" className="text-white hover:text-blue-200">Home</Link>
          <Link to="/checker" className="bg-white text-blue-700 px-4 py-2 rounded-md hover:bg-blue-100">
            Check Brand
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
