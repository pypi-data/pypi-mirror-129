#include <vector>
#include <tuple>
#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

// inflection starts here

using namespace std;

const vector<string> UNCOUNTABLES = {
    "equipment",
    "fish",
    "information",
    "jeans",
    "news",
    "money",
    "rice",
    "series",
    "sheep",
    "species"
};

const vector<tuple<string, bool, int, string>> PLURALS = {
    {"ox", true, 0, "en"},
    {"oxen", true, 0, ""},
    {"axis", true, 2, "es"},
    {"testis", true, 2, "es"},
    {"human", false, 0, "s"},
    {"man", false, 2, "en"},
    {"quiz", false, 0, "zes"},
    {"mice", false, 0, ""},
    {"lice", false, 0, ""},
    {"mouse", false, 4, "ice"},
    {"louse", false, 4, "ice"},
    {"passerby", false, 2, "sby"},
    {"passersby", false, 0, ""},
    {"matrix", false, 1, "ces"},
    {"vertex", false, 2, "ices"},
    {"index", false, 2, "ices"},
    {"x", false, 0, "es"},
    {"ch", false, 0, "es"},
    {"ss", false, 0, "es"},
    {"sh", false, 0, "es"},
    {"hive", false, 0, "s"},
    {"lf", false, 1, "ves"},
    {"rf", false, 1, "ves"},
    {"sis", false, 3, "ses"},
    {"rf", false, 1, "ves"},
    {"ta", false, 0, ""},
    {"ia", false, 0, ""},
    {"tum", false, 2, "a"},
    {"ium", false, 2, "a"},
    {"buffalo", false, 0, "es"},
    {"potato", false, 0, "es"},
    {"tomato", false, 0, "es"},
    {"bus", false, 0, "es"},
    {"alias", false, 0, "es"},
    {"status", false, 0, "es"},
    {"octopi", false, 0, ""},
    {"viri", false, 0, ""},
    {"octopus", false, 2, "i"},
    {"virus", false, 2, "i"},
    {"s", false, 0, ""},
};

const vector<tuple<string, bool, int, string>> SINGULARS = {
    {"oxen", true, 2, ""},
    {"axis", true, 0, ""},
    {"axes", true, 2, "is"},
    {"ies", false, 3, "y"},
    {"databases", false, 1, ""},
    {"men", false, 2, "an"},
    {"quizzes", false, 3, ""},
    {"matrices", false, 3, "x"},
    {"vertices", false, 4, "ex"},
    {"indices", false, 4, "ex"},
    {"passersby", false, 3, "by"},
    {"alias", false, 0, ""},
    {"aliases", false, 2, ""},
    {"status", false, 0, ""},
    {"statuses", false, 2, ""},
    {"octopus", false, 0, ""},
    {"octopi", false, 1, "us"},
    {"virus", false, 0, ""},
    {"viri", false, 1, "us"},
    {"crisis", false, 0, ""},
    {"crises", false, 2, "is"},
    {"testis", false, 0, ""},
    {"testes", false, 2, "is"},
    {"shoes", false, 1, ""},
    {"oes", false, 2, ""},
    {"bus", false, 0, ""},
    {"buses", false, 2, ""},
    {"slice", false, 0, ""},
    {"mice", false, 3, "ouse"},
    {"lice", false, 3, "ouse"},
    {"xes", false, 2, ""},
    {"ches", false, 2, ""},
    {"sses", false, 2, ""},
    {"shes", false, 2, ""},
    {"movies", false, 1, ""},
    {"lves", false, 3, "f"},
    {"rves", false, 3, "f"},
    {"tives", false, 1, ""},
    {"hives", false, 1, ""},
    {"ves", false, 3, "fe"},
    {"thesis", false, 0, ""},
    {"theses", false, 2, "is"},
    {"synopsis", false, 0, ""},
    {"synopses", false, 2, "is"},
    {"prognosis", false, 0, ""},
    {"prognoses", false, 2, "is"},
    {"parenthesis", false, 0, ""},
    {"parentheses", false, 2, "is"},
    {"diagnosis", false, 0, ""},
    {"diagnoses", false, 2, "is"},
    {"basis", false, 0, ""},
    {"bases", false, 2, "is"},
    {"analysis", false, 0, ""},
    {"analyses", false, 2, "is"},
    {"ta", false, 1, "um"},
    {"ia", false, 1, "um"},
    {"ss", false, 2, ""},
    {"s", false, 1, ""}
};

const size_t UNCOUNTABLES_SIZE = UNCOUNTABLES.size();
const size_t PLURALS_SIZE = PLURALS.size();
const size_t SINGULARS_SIZE = SINGULARS.size();

string lowercase(string str) {
    string retval = "";
    size_t length = str.length();
    for (int i = 0; i < length; i++) {
        retval.push_back(tolower(str.at(i)));
    }
    return retval;
}

string uppercase(string str) {
    string retval = "";
    size_t length = str.length();
    for (int i = 0; i < length; i++) {
        retval.push_back(toupper(str.at(i)));
    }
    return retval;
}

string _pascal_or_camel(string str, bool capitalize) {
    string retval = "";
    size_t length = str.length();
    bool cap = false;
    for (int i = 0; i < length; i++) {
        char character = str.at(i);
        if (character == '_') {
            cap = true;
        } else {
            if (cap) {
                retval.push_back(toupper(character));
            } else if (i == 0) {
                if (capitalize) {
                    retval.push_back(toupper(character));
                } else {
                    retval.push_back(tolower(character));
                }
            } else {
                retval.push_back(character);
            }
            cap = false;
        }
    }
    return retval;
}

string camelize(string str) {
    return _pascal_or_camel(str, false);
}

string pascalize(string str) {
    return _pascal_or_camel(str, true);
}

string underscore(string str) {
    string retval = "";
    size_t length = str.size();
    size_t lengthMinusOne = length - 1;
    bool continuousUppercase = false;
    bool firstAlnum = true;
    for (int i = 0; i < length; i++) {
        char character = str.at(i);
        if (character >= 'A' && character <= 'Z') {
            if (continuousUppercase) {
                if (i < lengthMinusOne) {
                    char next = str.at(i + 1);
                    if (!(next >= 'A' && next <= 'Z')) {
                        if (!firstAlnum) {
                            retval.push_back('_');
                        }
                        retval.push_back(tolower(character));
                        continuousUppercase = false;
                    } else {
                        retval.push_back(tolower(character));
                    }
                } else {
                    retval.push_back(tolower(character));
                }
            } else {
                if (i != 0) {
                    if (!firstAlnum) {
                        retval.push_back('_');
                    }
                }
                retval.push_back(tolower(character));
                continuousUppercase = true;
            }
        } else {
            retval.push_back(character);
            continuousUppercase = false;
        }
        if (firstAlnum) {
            if ((character >= 'A' && character <= 'Z')
                || (character >= 'a' && character <= 'z')
                || (character >= '0' && character <= '9')) {
                firstAlnum = false;
            }
        }
    }
    return retval;
}

string dasherize(string str) {
    string retval = "";
    size_t length = str.length();
    for (int i = 0; i < length; i++) {
        char character = str.at(i);
        if (character == '_') {
            retval.push_back('-');
        } else {
            retval.push_back(character);
        }
    }
    return retval;
}

bool isprefix(string prefix, string str) {
    return str.compare(0, prefix.size(), prefix) == 0;
}

bool issuffix(string suffix, string str) {
    size_t suffixSize = suffix.size();
    size_t strSize = str.size();
    if (suffixSize > strSize) { return false; }
    return str.compare(strSize - suffixSize, suffixSize, suffix) == 0;
}

string ordinal(int num) {
    int mod100 = num % 100;
    if (11 <= mod100 && mod100 <= 13) {
        return "th";
    }
    switch (num % 10) {
        case 1:
            return "st";
        case 2:
            return "nd";
        case 3:
            return "rd";
        default:
            return "th";
    }
}

string ordinalize(int num) {
    return to_string(num) + ordinal(num);
}

string pluralize(string str) {
    if (str.empty()) { return ""; }
    // check if str suffix is uncountable
    string lowercased = lowercase(str);
    for (int i = 0; i < UNCOUNTABLES_SIZE; i++) {
        if (issuffix(UNCOUNTABLES[i], lowercased)) {
            string retval = str;
            return retval;
        }
    }
    // make this singular word into plural
    // y special rule
    size_t length = lowercased.length();
    if (lowercased.back() == 'y') {
        if (length == 1) {
            return str + 's';
        }
        char secondLast = lowercased.at(length - 2);
        switch (secondLast) {
            case 'a':
                return str + 's';
            case 'e':
                return str + 's';
            case 'i':
                return str + 's';
            case 'o':
                return str + 's';
            case 'u':
                if (length >= 3) {
                    char thirdLast = lowercased.at(length - 3);
                    if (thirdLast == 'q') {
                        return str.substr(0, length - 1) + "ies";
                    } else {
                        return str + 's';
                    }
                } else {
                    return str + 's';
                }
            case 'y':
                return str + 's';
            default:
                return str.substr(0, length - 1) + "ies";
        }
    }
    // ff special rule
    // TODO
    // special rules in table
    for (int i = 0; i < PLURALS_SIZE; i++) {
        auto rule = PLURALS[i];
        string stem = get<0>(rule);
        bool whole = get<1>(rule);
        bool match;
        if (whole) {
            match = lowercased == stem;
        } else {
            match = issuffix(stem, lowercased);
        }
        if (match) {
            int replaceLength = get<2>(rule);
            string replacement = get<3>(rule);
            return str.substr(0, length - replaceLength) + replacement;
        }
        continue;
    }
    return str + 's';
}

string singularize(string str) {
    if (str.empty()) { return ""; }
    // check if str suffix is uncountable
    string lowercased = lowercase(str);
    for (int i = 0; i < UNCOUNTABLES_SIZE; i++) {
        if (issuffix(UNCOUNTABLES[i], lowercased)) {
            string retval = str;
            return retval;
        }
    }
    // make this plural word into singular
    size_t length = lowercased.length();
    // special rules in table
    for (int i = 0; i < SINGULARS_SIZE; i++) {
        auto rule = SINGULARS[i];
        string stem = get<0>(rule);
        bool whole = get<1>(rule);
        bool match;
        if (whole) {
            match = lowercased == stem;
        } else {
            match = issuffix(stem, lowercased);
        }
        if (match) {
            int replaceLength = get<2>(rule);
            string replacement = get<3>(rule);
            return str.substr(0, length - replaceLength) + replacement;
        }
        continue;
    }
    string retval = str;
    return retval;
}

string humanize(string str) {
    string retval = "";
    bool removeLastThree = issuffix("_id", str);
    size_t length = str.size();
    bool nextWordIsCamelize = true;
    bool isNextWord = true;
    bool lastCharIsWs = false;
    for (int i = 0; i < length; i++) {
        if (removeLastThree && i >= length - 3) {
            break;
        }
        char character = str.at(i);
        if (character == ' ' || character == '_') {
            if (isNextWord) {
                continue;
            }
            retval.push_back(' ');
            isNextWord = true;
            lastCharIsWs = true;
        } else if (character >= 'a' && character <= 'z' && nextWordIsCamelize) {
            retval.push_back(toupper(character));
            nextWordIsCamelize = false;
            isNextWord = false;
            lastCharIsWs = false;
        } else if (character >= 'A' && character <= 'Z' && !nextWordIsCamelize) {
            retval.push_back(tolower(character));
            isNextWord = false;
            lastCharIsWs = false;
        } else {
            retval.push_back(character);
            isNextWord = false;
            lastCharIsWs = false;
        }
    }
    return retval;
}

string parameterize(string str) {
    string retval = "";
    size_t length = str.size();
    bool wordStart = true;
    for (int i = 0; i < length; i++) {
        char character = str.at(i);
        if (('a' <= character && character <= 'z') ||
            ('A' <= character && character <= 'Z') ||
            ('0' <= character && character <= '9')) {
            retval.push_back(tolower(character));
            wordStart = false;
        } else {
            if (!wordStart) {
                retval.push_back('-');
                wordStart = true;
            }
        }
    }
    size_t retvalLength = retval.size();
    for (int i = (int)retvalLength - 1; i >= 0; i--) {
        char character = retval.at(i);
        if (('a' <= character && character <= 'z') ||
            ('A' <= character && character <= 'Z') ||
            ('0' <= character && character <= '9')) {
            break;
        } else {
            retval.pop_back();
        }
    }
    return retval;
}

string tableize(string str) {
    return pluralize(underscore(str));
}

string titleize(string str) {
    string retval = "";
    size_t length = str.size();
    bool wordStart = true;
    for (int i = 0; i < length; i++) {
        char character = str.at(i);
        if (('a' <= character && character <= 'z') ||
            ('A' <= character && character <= 'Z') ||
            ('0' <= character && character <= '9')) {
            if (wordStart) {
                retval.push_back(toupper(character));
            } else {
                retval.push_back(character);
            }
            wordStart = false;
        } else {
            if (!wordStart) {
                retval.push_back(' ');
                wordStart = true;
            }
        }
    }
    size_t retvalLength = retval.size();
    for (int i = (int)retvalLength - 1; i >= 0; i--) {
        char character = retval.at(i);
        if (('a' <= character && character <= 'z') ||
            ('A' <= character && character <= 'Z') ||
            ('0' <= character && character <= '9')) {
            break;
        } else {
            retval.pop_back();
        }
    }
    return retval;
}

// inflection ends here

namespace py = pybind11;

PYBIND11_MODULE(inflection, m) {
    m.doc() = "The inflection module";

    m.def("camelize", &camelize, "Camelized string.");

    m.def("pascalize", &pascalize, "Pascalized string.");

    m.def("underscore", &underscore, "Underscore string.");

    m.def("dasherize", &dasherize, "Dasherize string.");

    m.def("ordinal", &ordinal, "Ordinal string.");

    m.def("ordinalize", &ordinalize, "Ordinalize string.");

    m.def("pluralize", &pluralize, "Pluralized string.");

    m.def("singularize", &singularize, "Singularized string.");

    m.def("humanize", &humanize, "Humanized string.");

    m.def("parameterize", &parameterize, "Parameterized string.");

    m.def("tableize", &tableize, "Tableized string.");

    m.def("titleize", &titleize, "Titleized string.");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
