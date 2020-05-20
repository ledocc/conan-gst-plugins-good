#include <gst/gst.h>
#include <gst/gstplugin.h>

#include <iostream>
#include <string>
#include <vector>


bool test_plugin(const std::string & name)
{
    GstElement * plugin = gst_element_factory_make(name.data(), NULL);
    if (!plugin) {
        std::cerr << "failed to create "<<name<<" element" << std::endl;
        return false;
    } else {
        std::cout << name <<" has been created successfully" << std::endl;
    }
    gst_object_unref(GST_OBJECT(plugin));
    return true;
}


int main(int argc, char * argv[])
{
    gst_init(&argc, &argv);

    std::vector<std::string> plugins =
        {
#ifdef WITH_MPG123
         "mpg123audiodec",
#endif
#ifdef WITH_LAME
         "lamemp3enc",
#endif
         "alpha"
        };

    bool result = true;
    for (const auto & plugin : plugins)
    {
        result &= test_plugin(plugin);
    }

    return ! result;
}
