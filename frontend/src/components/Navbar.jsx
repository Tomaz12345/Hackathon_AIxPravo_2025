import { Link } from 'react-router-dom';
import { FaCheck } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 w-full bg-gradient-to-r from-blue-600 to-blue-800 p-4 shadow-md z-50">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="!text-white font-bold text-2xl flex items-center">
          <FaCheck className="mr-2" />
          BrandChecker
        </Link>
        <div className="space-x-4">
          <Link to="/" className="!text-white px-4 py-2 rounded-md hover:bg-blue-400">Home</Link>
          <Link to="/checker" className="!text-white px-4 py-2 rounded-md hover:bg-blue-400">
            Check Brand
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
