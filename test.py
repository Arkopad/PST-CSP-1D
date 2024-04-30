from ortools.linear_solver import pywraplp




def main():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return

    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    x0 = solver.IntVar(0.0, infinity, "x0")
    x1 = solver.IntVar(0.0, infinity, "x1")
    x2 = solver.IntVar(0.0, infinity, "x2")
    x3 = solver.IntVar(0.0, infinity, "x3")
    x4 = solver.IntVar(0.0, infinity, "x4")
    x5 = solver.IntVar(0.0, infinity, "x5")
    x6 = solver.IntVar(0.0, infinity, "x6")
    x7 = solver.IntVar(0.0, infinity, "x7")
    x8 = solver.IntVar(0.0, infinity, "x8")
    x9 = solver.IntVar(0.0, infinity, "x9")
    x10 = solver.IntVar(0.0, infinity, "x10")
    x11= solver.IntVar(0.0, infinity, "x11")
    x12= solver.IntVar(0.0, infinity, "x12")


    print("Number of variables =", solver.NumVariables())

    # x + 7 * y <= 17.5.
    solver.Add(3*x1 + 2*x3 + 1*x4 + 2*x5 + 1*x6 + 1*x8 + 1*x10 == 10)
    solver.Add(3*x2 + 1*x3 + 2*x4 + 1*x6 + 2*x7 + 1*x9 + 1*x11 == 12)
    solver.Add(1*x8 + 1*x9 + 1*x12 == 6)



    print("Number of constraints =", solver.NumConstraints())

    # Maximize x + 10 * y.
    solver.Minimize(1*x1 + 1*x2 + 1*x3 + 1*x4 + 1*x5 + 1*x6 + 1*x7 + 1*x8 + 1*x9 + 1*x10 + 1*x11 + 1*x12)

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("x0 =", solver.Objective().Value())
        print("x1 =", x1.solution_value())
        print("x2 =", x2.solution_value())
        print("x3 =", x3.solution_value())
        print("x4 =", x4.solution_value())
        print("x5 =", x5.solution_value())
        print("x6 =", x6.solution_value())
        print("x7 =", x7.solution_value())
        print("x8 =", x8.solution_value())
        print("x9 =", x9.solution_value())
        print("x10 =", x10.solution_value())
        print("x11 =", x11.solution_value())
        print("x12 =", x12.solution_value())



    else:
        print("The problem does not have an optimal solution.")

if __name__ == "__main__":
    main()