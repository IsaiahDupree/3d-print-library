# Orion / ANSYS engineering evidence

This directory contains the public evidence subset for the A/C Enclosure V4 screening run completed on Orion on 2026-09-20.

- Solver: ANSYS MAPDL 2022 R2 through the Orion `cad.freecad_fea` pipeline.
- Exact source: public V4 body STEP, SHA-256 `e84119d4285ede12fa56ab8cf4b2404c2a76e70c07955359e06313563581c844`.
- Load case: idealized 250 N rim compression; base fixed in all degrees of freedom.
- Material card: nominal isotropic PETG screening properties, not printer- or grade-calibrated.
- Mesh sweep: 6.0, 4.0, and 2.5 mm target sizes using SOLID187 tetrahedra.
- Finest result: 9.712 MPa peak averaged von Mises stress and 0.8198 mm maximum displacement.
- Convergence: displacement changed 0.38% from 4.0 to 2.5 mm; peak stress changed 21.6% and remains mesh-sensitive.

The full readable report is [`../files/ac-enclosure-v4-orion-ansys-screening-report.pdf`](../files/ac-enclosure-v4-orion-ansys-screening-report.pdf). `results.csv`, the three contours, `sweep.png`, `manifest.json`, and `orion-job.json` preserve the public numerical evidence and job contract.

This is a design screen, not a factor-of-safety claim, printed-part qualification, or approval for vehicle installation. It does not model FDM anisotropy, temperature, creep, water, fastener preload, vibration, impact, fatigue, or measured material allowables.
