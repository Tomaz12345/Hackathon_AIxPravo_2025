const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white p-4 mt-auto">
      <div className="container mx-auto text-center">
        <p>&copy; {new Date().getFullYear()} BrandChecker. All rights reserved.</p>
        <p className="text-gray-400 text-sm mt-1">
          This tool helps check trademark availability but does not guarantee registration success.
        </p>
      </div>
    </footer>
  );
};

export default Footer;