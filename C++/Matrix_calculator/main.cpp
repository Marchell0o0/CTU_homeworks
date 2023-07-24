#include <iostream>
#include <vector>
#include <sstream> 
#include <string>

using namespace std;


class Matrix {
public:
    vector<vector<int>> data;
    char operation;

    // Constructor
    Matrix() : operation('\0') {}  // Initialize operation with null character

    // Copy constructor for deep copy
    Matrix(const Matrix& m) : data(m.data), operation(m.operation) {}

    // Assignment operator for deep copy
    Matrix& operator=(const Matrix& m) {
        if (this != &m) { // protect against invalid self-assignment
            data = m.data;
            operation = m.operation;
        }
        return *this;
    }

    Matrix operator + (const Matrix& other) {
        if (data.size() != other.data.size() || data[0].size() != other.data[0].size()) {
            throw invalid_argument("Matrices must have the same dimensions for addition");
        }

        int rows = data.size();
        int cols = data[0].size();

        Matrix result;
        result.data.resize(rows, vector<int>(cols, 0));

        for (int r = 0; r < rows; ++r){
            for (int c = 0; c < cols; ++c){
                result.data[r][c] = data[r][c] + other.data[r][c];
            }
        }
        return result;
    }


    Matrix operator - (const Matrix& other) {
        if (data.size() != other.data.size() || data[0].size() != other.data[0].size()) {
            throw invalid_argument("Matrices must have the same dimensions for subtraction");
        }

        int rows = data.size();
        int cols = data[0].size();

        Matrix result;
        result.data.resize(rows, vector<int>(cols, 0));

        for (int r = 0; r < rows; ++r){
            for (int c = 0; c < cols; ++c){
                result.data[r][c] = data[r][c] - other.data[r][c];
            }
        }
        return result;
    }

    Matrix operator * (const Matrix& other) {
        if (data[0].size() != other.data.size()) {
            throw invalid_argument("Wrong dimensions for multiplication");
        }

        int rowsFirst = data.size();
        int colsFirst = data[0].size();
        int colsSecond = other.data[0].size();


        Matrix result;
        result.data.resize(rowsFirst, vector<int>(colsSecond, 0));

        for (int r = 0; r < rowsFirst; ++r){
            for (int c = 0; c < colsSecond; ++c){
                for (int k = 0; k < colsFirst; ++k){
                    result.data[r][c] += data[r][k] * other.data[k][c];
                }
            }
        }
        return result;
    }

    // Stream insertion operator for printing
    friend ostream& operator<<(ostream& os, const Matrix& matrix) {
        for (const auto& row : matrix.data) {
            // Print all but the last element with a trailing space
            for (size_t i = 0; i < row.size() - 1; ++i) {
                os << row[i] << ' ';
            }
            // Print the last element without a trailing space
            if (!row.empty()) {
                os << row.back();
            }
            os << '\n';
        }
        return os;
    }

    // Stream extraction operator for input
    friend istream& operator>>(istream& is, Matrix& matrix) {
        int columns = -1;  
        string line;
        vector<int> row;

        while(getline(is, line)){
            if (line.empty()){ continue; }

            string input;
            istringstream lineStream(line);
            bool operation = false;
            bool number_line = false;

            while (lineStream >> input){
                try{
                    int number;
                    number = stoi(input);
                    row.push_back(number);
                    number_line = true;                
                }
                // Something different than a number was caught
                catch (...){
                    if (number_line || (input != "+" && input != "-" && input != "*")){
                        throw invalid_argument("Invalid character or an unsupported operation");
                    } else {
                        operation = true;
                        matrix.operation = input[0];
                    }
                }
            }
            if (operation) { break; }
            matrix.data.push_back(row);
            if (columns != -1 && columns != static_cast<int>(row.size())){
                throw invalid_argument("Invalid matrix dimensions");
            }
            columns = row.size();
            row.clear();
        }
        return is;
    }
};

class Matrix_Array{
public:  
    int size;
    vector<Matrix> matrices;
    vector<char> operations;  

    Matrix_Array() : size(0), matrices(), operations() {}

    void add_matrix(const Matrix& m, const char op='\0'){
        matrices.push_back(m);
        if (op != '\0') {
            operations.push_back(op);
        }
        size = matrices.size();
    }

    Matrix calculate_result() {
        multiply();

        if (matrices.size() != operations.size() + 1) {
            throw invalid_argument("Operations count mismatch");
        }

        Matrix result = matrices[0];
        for (size_t i = 1; i < matrices.size(); ++i) {
            if (operations[i-1] == '+') {
                result = result + matrices[i];
            } else if (operations[i-1] == '-') {
                result = result - matrices[i];
            } else {
                throw invalid_argument("Unsupported operation");
            }
        }

        return result;
    }

    // Stream insertion operator for printing
    friend ostream& operator<<(ostream& os, const Matrix_Array& matrix_array) {
        int i = 0;
        for (const auto& matrix : matrix_array.matrices) {
            cout << "Matrix index: " << i << endl;
            i++;
            cout << matrix;
        }
        for (auto& elem : matrix_array.operations){
            cout << elem << " ";
        }
        cout << endl;
        return os;
    }
    private:
        void multiply(){
            Matrix result;
            for(int i = operations.size() - 1; i >= 0; i--) {
                if (operations[i] == '*'){
                    result = matrices[i] * matrices[i+1];
                    matrices[i] = result;
                    matrices.erase(matrices.begin()+i+1);
                    operations.erase(operations.begin()+i);
                }
            }
        }
};

int main() {
    Matrix_Array matrix_array;
    // cout << "While entering a matrix double enter is treated as the end of the matrix" << endl;
    int target;
    cin >> target;
    while(true){
        try {
            // cout << "Enter a matrix or end input with CTRL+D: " << endl;
            Matrix matrix;
            if (!(cin >> matrix)) {
                if(cin.eof()){
                    matrix_array.add_matrix(matrix); // No operation for the last matrix
                    break;
                } else {
                    throw invalid_argument("Incorrect matrix format");
                }
            }  
            matrix_array.add_matrix(matrix, matrix.operation);

        } catch (const invalid_argument& e) {
            cerr << "Invalid input: " << e.what() << endl;
        }
    }
    // cout << matrix_array;

    // cout << "Result" << endl;
    cout << matrix_array.calculate_result();

    return EXIT_SUCCESS;
}