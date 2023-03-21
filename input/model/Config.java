package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.core.consumer.shared.ConsumerProps;
import no.fintlabs.core.consumer.shared.resource.ConsumerConfig;
import org.springframework.stereotype.Component;

@Component
public class MODELConfig extends ConsumerConfig<MODEL_RESOURCE> {

    public MODELConfig(ConsumerProps consumerProps) {
        super(consumerProps);
    }

    @Override
    protected String domainName() {
        return "DOMAIN";
    }

    @Override
    protected String packageName() {
        return "PACKAGE";
    }

    @Override
    protected String resourceName() {
        return "MODEL_LOWER";
    }
}
