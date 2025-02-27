const Footer = () => {
  return (
    <footer className="fixed bottom-0 left-0 w-full bg-gray-900 text-white text-center p-4 shadow-md z-50">
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