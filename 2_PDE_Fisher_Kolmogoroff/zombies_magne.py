from dolfin import *
import matplotlib.pyplot as plt

def pyplot(u, **args):
    SIR = u.vector().array().reshape(N+1,3)
    plt.plot(x, SIR)
    if 'title' in args:
        plt.title(args['title'])
    plt.legend(('Humans', 'Zombies', 'Dead'))
    plt.show()

# discretization paramters
N  = 200  # mesh size
T  = 10.0
dt = .05
theta = .5

mesh = UnitIntervalMesh(N)
x = mesh.coordinates().reshape((N+1,))

# model parameters:
cI   = .05
cS   = .005
cR   = 0.0
rIS  = 1.0
rS   = .25

# Initial data
p0 = Expression('1.0')
u0 = Expression(('1.-(1.-4*x[0])*(x[0]<=.25)',
                 '(1.-4*x[0])*(x[0]<=.25)',
                 '0.'))

V = VectorFunctionSpace(mesh, 'CG', 1, dim = 3)
Q = FunctionSpace(mesh, 'CG', 1)
u,  v = Function(V), TestFunction(V)
p = interpolate(p0, Q)
Lp=  Expression('-2*pi*pi*cos(pi*x[0])')

# model is defined here in the form: du/dt = f(u)
def f(u,v):
    form =(- rIS * u[0]*u[1]*v[0]               -cS * inner(grad(u[0]), grad(v[0]))   
           + rIS * u[0]*u[1]*v[1] -rS*u[1]*v[1] -cI * inner(grad(u[1]), grad(v[1]))
           +                       rS*u[1]*v[2] -cR * inner(grad(u[2]), grad(v[2]))
           ) * dx
    return form

t, n = 0, 0
u_ = interpolate(u0, V)
u.assign(u_)
pyplot(u, title = 'Initial data')
while t < T:
    a = inner(u ,v) * dx  -dt*theta*f(u,v)
    L = inner(u_,v) * dx  +dt*(1.-theta)*f(u_,v)
    F = a - L
    solve(F == 0, u)
    u_.assign(u)    
    t += dt
    n += 1
    print t
    if n%40 == 0:
        pyplot(u, title = 'time = {}'.format(t))


    

    


