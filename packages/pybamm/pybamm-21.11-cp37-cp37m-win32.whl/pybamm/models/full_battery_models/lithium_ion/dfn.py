#
# Doyle-Fuller-Newman (DFN) Model
#
import pybamm
from .base_lithium_ion_model import BaseModel


class DFN(BaseModel):
    """Doyle-Fuller-Newman (DFN) model of a lithium-ion battery, from [1]_.

    Parameters
    ----------
    options : dict, optional
        A dictionary of options to be passed to the model.
    name : str, optional
        The name of the model.
    build :  bool, optional
        Whether to build the model on instantiation. Default is True. Setting this
        option to False allows users to change any number of the submodels before
        building the complete model (submodels cannot be changed after the model is
        built).

    References
    ----------
    .. [1] SG Marquis, V Sulzer, R Timms, CP Please and SJ Chapman. “An asymptotic
           derivation of a single particle model with electrolyte”. Journal of The
           Electrochemical Society, 166(15):A3693–A3706, 2019


    **Extends:** :class:`pybamm.lithium_ion.BaseModel`
    """

    def __init__(self, options=None, name="Doyle-Fuller-Newman model", build=True):
        super().__init__(options, name)
        # For degradation models we use the full form since this is a full-order model
        self.x_average = False

        self.set_external_circuit_submodel()
        self.set_porosity_submodel()
        self.set_interface_utilisation_submodel()
        self.set_crack_submodel()
        self.set_active_material_submodel()
        self.set_tortuosity_submodels()
        self.set_convection_submodel()
        self.set_interfacial_submodel()
        self.set_other_reaction_submodels_to_zero()
        self.set_particle_submodel()
        self.set_solid_submodel()
        self.set_electrolyte_submodel()
        self.set_thermal_submodel()
        self.set_current_collector_submodel()
        self.set_sei_submodel()
        self.set_lithium_plating_submodel()

        if self.half_cell:
            # This also removes "negative electrode" submodels, so should be done last
            self.set_li_metal_counter_electrode_submodels()

        if build:
            self.build_model()

        pybamm.citations.register("Doyle1993")

    def set_convection_submodel(self):

        self.submodels[
            "transverse convection"
        ] = pybamm.convection.transverse.NoConvection(self.param, self.options)
        self.submodels[
            "through-cell convection"
        ] = pybamm.convection.through_cell.NoConvection(self.param, self.options)

    def set_interfacial_submodel(self):

        self.submodels["negative interface"] = pybamm.interface.ButlerVolmer(
            self.param, "Negative", "lithium-ion main", self.options
        )
        self.submodels["positive interface"] = pybamm.interface.ButlerVolmer(
            self.param, "Positive", "lithium-ion main", self.options
        )

    def set_particle_submodel(self):

        if isinstance(self.options["particle"], str):
            particle_left = self.options["particle"]
            particle_right = self.options["particle"]
        else:
            particle_left, particle_right = self.options["particle"]
        for particle_side, domain in [
            [particle_left, "Negative"],
            [particle_right, "Positive"],
        ]:
            if self.options["particle size"] == "single":
                if particle_side == "Fickian diffusion":
                    self.submodels[
                        domain.lower() + " particle"
                    ] = pybamm.particle.no_distribution.FickianDiffusion(
                        self.param,
                        domain,
                        self.options,
                    )
                elif particle_side in [
                    "uniform profile",
                    "quadratic profile",
                    "quartic profile",
                ]:
                    self.submodels[
                        domain.lower() + " particle"
                    ] = pybamm.particle.no_distribution.PolynomialProfile(
                        self.param,
                        domain,
                        particle_side,
                        self.options,
                    )
            elif self.options["particle size"] == "distribution":
                if particle_side == "Fickian diffusion":
                    self.submodels[
                        domain.lower() + " particle"
                    ] = pybamm.particle.size_distribution.FickianDiffusion(
                        self.param, domain
                    )
                elif particle_side == "uniform profile":
                    self.submodels[
                        domain.lower() + " particle"
                    ] = pybamm.particle.size_distribution.UniformProfile(
                        self.param,
                        domain,
                    )

    def set_solid_submodel(self):

        if self.options["surface form"] == "false":
            submod_n = pybamm.electrode.ohm.Full(self.param, "Negative", self.options)
            submod_p = pybamm.electrode.ohm.Full(self.param, "Positive", self.options)
        else:
            submod_n = pybamm.electrode.ohm.SurfaceForm(self.param, "Negative")
            submod_p = pybamm.electrode.ohm.SurfaceForm(self.param, "Positive")

        self.submodels["negative electrode potential"] = submod_n
        self.submodels["positive electrode potential"] = submod_p

        # Set the counter-electrode model for the half-cell model
        # The negative electrode model will be ignored
        if self.half_cell:
            if self.options["SEI"] in ["none", "constant"]:
                self.submodels[
                    "counter electrode surface potential difference"
                ] = pybamm.electrolyte_conductivity.surface_potential_form.Explicit(
                    self.param, "Negative", self.options
                )
                self.submodels[
                    "counter electrode potential"
                ] = pybamm.electrode.ohm.LithiumMetalExplicit(self.param, self.options)
            else:
                self.submodels[
                    "counter electrode potential"
                ] = pybamm.electrode.ohm.LithiumMetalSurfaceForm(
                    self.param, self.options
                )

    def set_electrolyte_submodel(self):

        surf_form = pybamm.electrolyte_conductivity.surface_potential_form

        self.submodels["electrolyte diffusion"] = pybamm.electrolyte_diffusion.Full(
            self.param, self.options
        )

        if self.options["electrolyte conductivity"] not in ["default", "full"]:
            raise pybamm.OptionError(
                "electrolyte conductivity '{}' not suitable for DFN".format(
                    self.options["electrolyte conductivity"]
                )
            )

        if self.options["surface form"] == "false":
            self.submodels[
                "electrolyte conductivity"
            ] = pybamm.electrolyte_conductivity.Full(self.param, self.options)
            surf_model = surf_form.Explicit
        elif self.options["surface form"] == "differential":
            surf_model = surf_form.FullDifferential
        elif self.options["surface form"] == "algebraic":
            surf_model = surf_form.FullAlgebraic

        for domain in ["Negative", "Separator", "Positive"]:
            self.submodels[
                domain.lower() + " surface potential difference"
            ] = surf_model(self.param, domain, self.options)
