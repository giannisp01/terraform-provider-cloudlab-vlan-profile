# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the InstaGENI library.
import geni.rspec.igext as ig
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

pc.defineParameter(
    "name", "VLAN Name",
    portal.ParameterType.STRING,
    longDescription="A shared VLAN name (functions as a private key allowing other experiments to connect to this VLAN). Must be fewer than 32 alphanumeric characters."),
params = pc.bindParameters()

if params.name.strip() == '':
    err = portal.ParameterError(
        "VLAN name not defined",
        ['name'])
    pc.reportError(err)

pc.verifyParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

tour = ig.Tour()
tour.Description(ig.Tour.TEXT, "Create a shared vlan.")
request.addTour(tour)

sharedvlan = pg.Link('shared-vlan')
sharedvlan.createSharedVlan(params.name)
sharedvlan.link_multiplexing = True
sharedvlan.best_effort = True

request.addResource(sharedvlan)

pc.printRequestRSpec(request)
