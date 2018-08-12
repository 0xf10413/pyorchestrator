#include <boost/python.hpp>
#include <iostream>

using namespace boost::python;

class Singleton
{
private:
  Singleton ()
  {
    std::cout << "Singleton initialized in PID=" << getpid() << std::endl;
  }
public:

  static Singleton &getInstance()
  {
    static Singleton instance;
    return instance;
  }

  int add(int a, int b)
  {
    sleep(2);
    int result = a + b;
    if (result < 0)
      throw std::runtime_error("Oh no! A negative value!");
    return result;
  }
};


BOOST_PYTHON_MODULE(fclass)
{
  class_<Singleton>("S", no_init)
    .def("get", &Singleton::getInstance,
        return_value_policy<reference_existing_object>())
    .staticmethod("get")
    .def("add", &Singleton::add)
    ;
}
